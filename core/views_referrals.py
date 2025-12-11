from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count

from .serializers import ReferralUserSummarySerializer
from .models import WalletTransaction

User = get_user_model()


class ReferralAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # All invited users
        referred_users = (
            User.objects.filter(referred_by=user)
            .annotate(
                tasks_completed=Count("user_tasks", filter=None),
                total_earned=Sum(
                    "wallet_transactions__coins",
                    filter=None
                )
            )
            .order_by("-date_joined")
        )

        # Summary data for each referral
        user_summaries = []
        for u in referred_users:
            user_summaries.append({
                "id": u.id,
                "username": u.username,
                "joined": u.date_joined,
                "coins_balance": u.coins_balance,
                "fraud_score": u.fraud_score,
                "tasks_completed": u.tasks_completed or 0,
                "total_earned_coins": u.total_earned or 0,
            })

        # Total referral earnings
        referral_earnings = WalletTransaction.objects.filter(
            user=user,
            type="referral"
        ).aggregate(total=Sum("coins"))["total"] or 0

        data = {
            "total_referred_users": referred_users.count(),
            "total_referral_earnings": referral_earnings,
            "referred_users": user_summaries,
        }

        return Response(data)
