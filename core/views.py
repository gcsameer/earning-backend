from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import PermissionDenied

from .models import Task, UserTask, WalletTransaction, WithdrawRequest, Settings
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    TaskSerializer,
    WalletTransactionSerializer,
    WithdrawRequestSerializer,
)
from .utils import check_task_speed, check_daily_task_limit

User = get_user_model()


# -----------------------------
#  HELPERS
# -----------------------------
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")


# -----------------------------
#  AUTH
# -----------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["coins_balance"] = user.coins_balance
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
#  USER PROFILE
# -----------------------------
class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


# -----------------------------
#  TASK SYSTEM
# -----------------------------
class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(is_active=True).order_by('id')
        # Log for debugging
        import logging
        logger = logging.getLogger(__name__)
        task_list = list(tasks.values('id', 'type', 'title', 'is_active'))
        logger.info(f"TaskListView: Returning {len(task_list)} tasks: {task_list}")
        return Response(TaskSerializer(tasks, many=True).data)


class TaskStartView(APIView):
    def post(self, request, task_id):

        # DAILY LIMIT CHECK
        check_daily_task_limit(request.user)

        try:
            task = Task.objects.get(id=task_id, is_active=True)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        ip = get_client_ip(request)
        device_id = request.data.get("device_id")

        user_task = UserTask.objects.create(
            user=request.user,
            task=task,
            status="pending",
            ip_address=ip,
            device_id=device_id,
        )

        return Response(
            {"message": "Task started", "user_task_id": user_task.id, "task": TaskSerializer(task).data},
            status=status.HTTP_201_CREATED,
        )


class TaskCompleteView(APIView):
    def post(self, request, user_task_id):
        try:
            user_task = UserTask.objects.get(id=user_task_id, user=request.user, status="pending")
        except UserTask.DoesNotExist:
            return Response({"detail": "Task not found or already completed"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # DAILY EARNING LIMIT
        if not user.can_earn_now(max_per_day=100):
            raise PermissionDenied("Daily earning limit reached. Try again tomorrow.")

        # MARK COMPLETED
        user_task.status = "completed"
        user_task.completed_at = timezone.now()
        user_task.save()

        # FRAUD CHECK
        try:
            check_task_speed(user_task)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        reward = user_task.task.reward_coins

        # UPDATE counters
        user.register_earn()
        user.coins_balance += reward
        user.save(update_fields=["coins_balance"])

        WalletTransaction.objects.create(
            user=user,
            type="earn",
            coins=reward,
            note=f"Completed task {user_task.task.title}",
        )

        return Response({"message": "Task completed", "reward_coins": reward})


# -----------------------------
#  WALLET SYSTEM
# -----------------------------
class WalletView(APIView):
    def get(self, request):
        user = request.user

        rate = float(Settings.get_value("COIN_TO_RS_RATE", "0.05"))
        balance_rs = user.coins_balance * rate

        tx = WalletTransaction.objects.filter(user=user).order_by("-created_at")[:50]

        return Response({
            "coins_balance": user.coins_balance,
            "approx_balance_rs": round(balance_rs, 2),
            "coin_to_rs_rate": rate,
            "transactions": WalletTransactionSerializer(tx, many=True).data,
        })


# -----------------------------
#  WITHDRAW SYSTEM
# -----------------------------
class WithdrawRequestView(APIView):
    def post(self, request):
        user = request.user

        amount_rs = request.data.get("amount_rs")
        method = request.data.get("method")
        account_id = request.data.get("account_id")

        if not amount_rs or not method or not account_id:
            return Response({"detail": "amount_rs, method, account_id are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            amount_rs = float(amount_rs)
        except:
            return Response({"detail": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        rate = float(Settings.get_value("COIN_TO_RS_RATE", "0.05"))
        min_rs = float(Settings.get_value("MIN_WITHDRAW_RS", "50"))

        if amount_rs < min_rs:
            return Response({"detail": f"Minimum withdraw is Rs {min_rs}"}, status=status.HTTP_400_BAD_REQUEST)

        coins_needed = int(amount_rs / rate)

        if user.coins_balance < coins_needed:
            return Response({"detail": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct coins
        user.coins_balance -= coins_needed
        user.save()

        WithdrawRequest.objects.create(
            user=user,
            amount_rs=amount_rs,
            method=method,
            account_id=account_id,
        )

        WalletTransaction.objects.create(
            user=user,
            type="withdraw",
            coins=-coins_needed,
            amount_rs=amount_rs,
            note=f"Withdraw request via {method}",
        )

        return Response({"message": "Withdraw request created"}, status=status.HTTP_201_CREATED)


class UserWithdrawListView(APIView):
    def get(self, request):
        w = WithdrawRequest.objects.filter(user=request.user).order_by("-created_at")
        return Response(WithdrawRequestSerializer(w, many=True).data)
