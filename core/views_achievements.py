"""
Achievement/Badge system for gamification.
"""
from django.utils import timezone
from django.db.models import Count, Sum
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserTask, WalletTransaction


class AchievementsView(APIView):
    """
    Get user achievements and badges.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        achievements = []

        # Total Earnings Achievements
        total_earned = WalletTransaction.objects.filter(
            user=user,
            type__in=["earn", "bonus", "referral"]
        ).aggregate(total=Sum("coins"))["total"] or 0

        if total_earned >= 1000:
            achievements.append({
                "id": "earner_1000",
                "name": "💰 First Thousand",
                "description": "Earned 1,000 coins",
                "icon": "💰",
                "unlocked": True
            })
        if total_earned >= 5000:
            achievements.append({
                "id": "earner_5000",
                "name": "💵 Big Earner",
                "description": "Earned 5,000 coins",
                "icon": "💵",
                "unlocked": True
            })
        if total_earned >= 10000:
            achievements.append({
                "id": "earner_10000",
                "name": "💎 Coin Master",
                "description": "Earned 10,000 coins",
                "icon": "💎",
                "unlocked": True
            })

        # Task Completion Achievements
        total_tasks = UserTask.objects.filter(user=user, status="completed").count()
        
        if total_tasks >= 10:
            achievements.append({
                "id": "tasker_10",
                "name": "🎯 Task Starter",
                "description": "Completed 10 tasks",
                "icon": "🎯",
                "unlocked": True
            })
        if total_tasks >= 50:
            achievements.append({
                "id": "tasker_50",
                "name": "⭐ Task Master",
                "description": "Completed 50 tasks",
                "icon": "⭐",
                "unlocked": True
            })
        if total_tasks >= 100:
            achievements.append({
                "id": "tasker_100",
                "name": "🏆 Task Legend",
                "description": "Completed 100 tasks",
                "icon": "🏆",
                "unlocked": True
            })

        # Streak Achievements
        if user.login_streak >= 7:
            achievements.append({
                "id": "streak_7",
                "name": "🔥 Week Warrior",
                "description": "7 day login streak",
                "icon": "🔥",
                "unlocked": True
            })
        if user.login_streak >= 30:
            achievements.append({
                "id": "streak_30",
                "name": "💪 Month Master",
                "description": "30 day login streak",
                "icon": "💪",
                "unlocked": True
            })

        # Referral Achievements
        total_referrals = user.referrals.count()
        
        if total_referrals >= 5:
            achievements.append({
                "id": "referrer_5",
                "name": "👥 Social Butterfly",
                "description": "Referred 5 friends",
                "icon": "👥",
                "unlocked": True
            })
        if total_referrals >= 20:
            achievements.append({
                "id": "referrer_20",
                "name": "🌟 Influencer",
                "description": "Referred 20 friends",
                "icon": "🌟",
                "unlocked": True
            })

        # Withdrawal Achievements
        withdrawals = user.withdrawals.filter(status__in=["approved", "paid"]).count()
        
        if withdrawals >= 1:
            achievements.append({
                "id": "withdrawer_1",
                "name": "💸 First Withdrawal",
                "description": "Made your first withdrawal",
                "icon": "💸",
                "unlocked": True
            })
        if withdrawals >= 10:
            achievements.append({
                "id": "withdrawer_10",
                "name": "💳 Regular Earner",
                "description": "Made 10 withdrawals",
                "icon": "💳",
                "unlocked": True
            })

        # Calculate progress for locked achievements
        locked_achievements = []

        # Next earning milestone
        next_earning = 1000 if total_earned < 1000 else (5000 if total_earned < 5000 else (10000 if total_earned < 10000 else None))
        if next_earning:
            locked_achievements.append({
                "id": f"earner_{next_earning}",
                "name": f"💰 Earn {next_earning} Coins",
                "description": f"Earn {next_earning} total coins",
                "icon": "💰",
                "unlocked": False,
                "progress": total_earned,
                "target": next_earning
            })

        # Next task milestone
        next_task = 10 if total_tasks < 10 else (50 if total_tasks < 50 else (100 if total_tasks < 100 else None))
        if next_task:
            locked_achievements.append({
                "id": f"tasker_{next_task}",
                "name": f"🎯 Complete {next_task} Tasks",
                "description": f"Complete {next_task} tasks",
                "icon": "🎯",
                "unlocked": False,
                "progress": total_tasks,
                "target": next_task
            })

        return Response({
            "unlocked": achievements,
            "locked": locked_achievements,
            "total_unlocked": len(achievements),
            "total_available": len(achievements) + len(locked_achievements)
        }, status=status.HTTP_200_OK)

