"""
Daily and weekly challenges system.
"""
from django.utils import timezone
from django.db.models import Count, Sum, Q
from datetime import timedelta
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserTask, WalletTransaction, Settings, DailyChallengeClaim


class DailyChallengesView(APIView):
    """
    Get and track daily challenges.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # Challenge 1: Complete 3 tasks today
        tasks_today = UserTask.objects.filter(
            user=user,
            status="completed",
            completed_at__date=today
        ).count()
        challenge_1_complete = tasks_today >= 3
        challenge_1_reward = 30 if challenge_1_complete else 0

        # Challenge 2: Earn 100 coins today
        coins_today = WalletTransaction.objects.filter(
            user=user,
            type__in=["earn", "bonus", "referral"],
            created_at__date=today
        ).aggregate(total=Sum("coins"))["total"] or 0
        challenge_2_complete = coins_today >= 100
        challenge_2_reward = 50 if challenge_2_complete else 0

        # Challenge 3: Login streak (already tracked)
        challenge_3_complete = user.login_streak >= 3
        challenge_3_reward = 20 if challenge_3_complete else 0

        # Check which challenges have been claimed today
        claimed_today = DailyChallengeClaim.objects.filter(
            user=user,
            claimed_date=today
        ).values_list('challenge_id', flat=True)

        challenges = [
            {
                "id": "complete_3_tasks",
                "title": "Complete 3 Tasks",
                "description": "Finish 3 tasks today",
                "progress": tasks_today,
                "target": 3,
                "reward": 30,
                "completed": challenge_1_complete,
                "claimed": "complete_3_tasks" in claimed_today
            },
            {
                "id": "earn_100_coins",
                "title": "Earn 100 Coins",
                "description": "Earn 100 coins today",
                "progress": coins_today,
                "target": 100,
                "reward": 50,
                "completed": challenge_2_complete,
                "claimed": "earn_100_coins" in claimed_today
            },
            {
                "id": "streak_3_days",
                "title": "3 Day Streak",
                "description": "Maintain a 3 day login streak",
                "progress": user.login_streak,
                "target": 3,
                "reward": 20,
                "completed": challenge_3_complete,
                "claimed": "streak_3_days" in claimed_today
            }
        ]

        total_rewards = sum(c["reward"] for c in challenges if c["completed"] and not c["claimed"])

        return Response({
            "challenges": challenges,
            "total_rewards_available": total_rewards,
            "date": today.isoformat()
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """Claim challenge reward."""
        challenge_id = request.data.get("challenge_id")
        user = request.user
        today = timezone.now().date()

        # Check if already claimed today
        if DailyChallengeClaim.objects.filter(
            user=user,
            challenge_id=challenge_id,
            claimed_date=today
        ).exists():
            return Response(
                {"detail": "This challenge reward has already been claimed today. Try again tomorrow."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Re-check challenge completion
        if challenge_id == "complete_3_tasks":
            tasks_today = UserTask.objects.filter(
                user=user,
                status="completed",
                completed_at__date=today
            ).count()
            if tasks_today >= 3:
                reward = 30
                user.coins_balance += reward
                user.save(update_fields=["coins_balance"])
                WalletTransaction.objects.create(
                    user=user,
                    type="bonus",
                    coins=reward,
                    note="Daily challenge: Complete 3 tasks"
                )
                # Mark as claimed
                DailyChallengeClaim.objects.create(
                    user=user,
                    challenge_id=challenge_id,
                    claimed_date=today
                )
                return Response({
                    "message": "Challenge reward claimed!",
                    "reward": reward,
                    "new_balance": user.coins_balance
                })

        elif challenge_id == "earn_100_coins":
            coins_today = WalletTransaction.objects.filter(
                user=user,
                type__in=["earn", "bonus", "referral"],
                created_at__date=today
            ).aggregate(total=Sum("coins"))["total"] or 0
            if coins_today >= 100:
                reward = 50
                user.coins_balance += reward
                user.save(update_fields=["coins_balance"])
                WalletTransaction.objects.create(
                    user=user,
                    type="bonus",
                    coins=reward,
                    note="Daily challenge: Earn 100 coins"
                )
                # Mark as claimed
                DailyChallengeClaim.objects.create(
                    user=user,
                    challenge_id=challenge_id,
                    claimed_date=today
                )
                return Response({
                    "message": "Challenge reward claimed!",
                    "reward": reward,
                    "new_balance": user.coins_balance
                })

        elif challenge_id == "streak_3_days":
            if user.login_streak >= 3:
                reward = 20
                user.coins_balance += reward
                user.save(update_fields=["coins_balance"])
                WalletTransaction.objects.create(
                    user=user,
                    type="bonus",
                    coins=reward,
                    note="Daily challenge: 3 day streak"
                )
                # Mark as claimed
                DailyChallengeClaim.objects.create(
                    user=user,
                    challenge_id=challenge_id,
                    claimed_date=today
                )
                return Response({
                    "message": "Challenge reward claimed!",
                    "reward": reward,
                    "new_balance": user.coins_balance
                })

        return Response(
            {"detail": "Challenge not completed yet"},
            status=status.HTTP_400_BAD_REQUEST
        )

