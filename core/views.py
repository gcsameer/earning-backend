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


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


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


class MeView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(is_active=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskStartView(APIView):
    def post(self, request, task_id):
        # Optional extra guard: daily task limit BEFORE starting a new task
        check_daily_task_limit(request.user)

        try:
            task = Task.objects.get(id=task_id, is_active=True)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        ip = get_client_ip(request)
        device_id = request.data.get("device_id")

        user_task = UserTask.objects.create(
            user=request.user,
            task=task,
            status="pending",
            ip_address=ip,
            device_id=device_id,
        )

        # You already have this protection; leaving it here is fine too
        # (if you prefer only one call, you can remove this line)
        check_daily_task_limit(request.user)

        return Response(
            {
                "message": "Task started",
                "user_task_id": user_task.id,
                "task": TaskSerializer(task).data,
            },
            status=status.HTTP_201_CREATED,
        )


class TaskCompleteView(APIView):
    def post(self, request, user_task_id):
        try:
            user_task = UserTask.objects.get(
                id=user_task_id,
                user=request.user,
                status="pending",
            )
        except UserTask.DoesNotExist:
            return Response(
                {"detail": "User task not found or already completed"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        # 🔒 FRAUD / DAILY LIMIT CHECK (uses methods on your User model)
        # If you added can_earn_now(max_per_day=...) on User
        if hasattr(user, "can_earn_now") and not user.can_earn_now(max_per_day=100):
            raise PermissionDenied(
                "Daily earning limit reached. Try again tomorrow."
            )

        user_task.status = "completed"
        user_task.completed_at = timezone.now()
        user_task.save()

        # Existing anti-cheat: checks task duration / speed
        check_task_speed(user_task)

        reward = user_task.task.reward_coins

        # Update fraud counters if you implemented register_earn on User
        if hasattr(user, "register_earn"):
            # IMPORTANT: register_earn should only update tracking fields,
            # not coins_balance itself – we do the coin increment below.
            user.register_earn()

        # Add reward to user's coin balance
        user.coins_balance += reward
        user.save()

        WalletTransaction.objects.create(
            user=user,
            type="earn",
            coins=reward,
            note=f"Completed task {user_task.task.title}",
        )

        return Response({"message": "Task completed", "reward_coins": reward})


class WalletView(APIView):
    def get(self, request):
        user = request.user
        rate_str = Settings.get_value("COIN_TO_RS_RATE", "0.05")
        try:
            rate = float(rate_str)
        except ValueError:
            rate = 0.05

        balance_rs = user.coins_balance * rate

        transactions = (
            WalletTransaction.objects.filter(user=user)
            .order_by("-created_at")[:50]
        )
        tx_serializer = WalletTransactionSerializer(transactions, many=True)

        return Response(
            {
                "coins_balance": user.coins_balance,
                "approx_balance_rs": round(balance_rs, 2),
                "coin_to_rs_rate": rate,
                "transactions": tx_serializer.data,
            }
        )


class WithdrawRequestView(APIView):
    def post(self, request):
        user = request.user
        amount_rs = request.data.get("amount_rs")
        method = request.data.get("method")
        account_id = request.data.get("account_id")

        if not amount_rs or not method or not account_id:
            return Response(
                {"detail": "amount_rs, method, account_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount_rs = float(amount_rs)
        except ValueError:
            return Response(
                {"detail": "Invalid amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rate_str = Settings.get_value("COIN_TO_RS_RATE", "0.05")
        try:
            rate = float(rate_str)
        except ValueError:
            rate = 0.05

        min_withdraw_rs_str = Settings.get_value("MIN_WITHDRAW_RS", "50")
        min_withdraw_rs = float(min_withdraw_rs_str)

        if amount_rs < min_withdraw_rs:
            return Response(
                {"detail": f"Minimum withdraw is Rs {min_withdraw_rs}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        coins_needed = int(amount_rs / rate)

        if user.coins_balance < coins_needed:
            return Response(
                {"detail": "Insufficient balance"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deduct coins immediately
        user.coins_balance -= coins_needed
        user.save()

        # Status/admin_note/processed_at are handled in the model
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

        return Response(
            {"message": "Withdraw request created"},
            status=status.HTTP_201_CREATED,
        )


class UserWithdrawListView(APIView):
    def get(self, request):
        withdraws = (
            WithdrawRequest.objects.filter(user=request.user)
            .order_by("-created_at")
        )
        serializer = WithdrawRequestSerializer(withdraws, many=True)
        return Response(serializer.data)
