from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class ReferralAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        referred_users = (
            User.objects.filter(referred_by=user)
            .order_by("-date_joined")
        )

        data = {
            "my_ref_code": user.ref_code,          # <- your own code
            "total_referred": referred_users.count(),
            "users": [
                {
                    "username": u.username,
                    "joined": u.date_joined,
                    "coins": u.coins_balance,
                }
                for u in referred_users
            ],
        }
        return Response(data)
