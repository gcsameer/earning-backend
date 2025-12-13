from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import WalletTransaction, Settings


class DailyBonusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Check bonus status without claiming.
        Useful for frontend to show:
        - "Claim now"
        - "Come back tomorrow"
        """
        user = request.user
        today = timezone.now().date()

        already_claimed = user.daily_bonus_claimed == today

        # Get bonus amount from Settings table
        bonus_str = Settings.get_value("DAILY_BONUS_COINS", "20")
        try:
            bonus = int(bonus_str)
        except ValueError:
            bonus = 20

        return Response({
            "already_claimed": already_claimed,
            "bonus_amount": bonus,
            "last_claimed": user.daily_bonus_claimed,
        })

    def post(self, request):
        """
        Claim the daily reward.
        """
        user = request.user
        today = timezone.now().date()

        # Check if already claimed
        if user.daily_bonus_claimed == today:
            return Response(
                {"detail": "Daily bonus already claimed today."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Load bonus amount
        bonus_str = Settings.get_value("DAILY_BONUS_COINS", "20")
        try:
            bonus_coins = int(bonus_str)
        except ValueError:
            bonus_coins = 20

        # Apply coins to wallet
        user.coins_balance += bonus_coins
        user.daily_bonus_claimed = today
        user.save(update_fields=["coins_balance", "daily_bonus_claimed"])

        # Record in wallet transactions
        WalletTransaction.objects.create(
            user=user,
            type="bonus",
            coins=bonus_coins,
            note="Daily login bonus",
        )

        return Response(
            {
                "message": "Daily bonus claimed successfully",
                "bonus_coins": bonus_coins,
                "new_balance": user.coins_balance,
            },
            status=status.HTTP_200_OK,
        )
