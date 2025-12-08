from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date

class DailyBonusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = date.today()

        if user.daily_bonus_claimed == today:
            return Response({"detail": "Bonus already claimed today"}, status=400)

        bonus = 20
        user.coins_balance += bonus
        user.daily_bonus_claimed = today
        user.save()

        return Response({"message": "Bonus claimed!", "bonus": bonus})
