from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WalletTransaction

User = get_user_model()


class ReferralAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        referred_users = (
            User.objects.filter(referred_by=user)
            .order_by("-date_joined")
        )

        # Calculate total coins earned from referrals
        referral_transactions = WalletTransaction.objects.filter(
            user=user,
            type="referral"
        )
        total_referral_coins = sum(t.coins for t in referral_transactions)

        # Get coins earned per referred user (50 coins per referral)
        referral_coins_per_user = 50

        data = {
            "my_ref_code": user.ref_code,
            "total_referred": referred_users.count(),
            "total_referral_coins": total_referral_coins,  # Total coins earned from referrals
            "users": [
                {
                    "username": u.username,
                    "joined": u.date_joined,
                    "referral_coins_earned": referral_coins_per_user,  # Coins earned from this referral (50)
                }
                for u in referred_users
            ],
        }
        return Response(data)
