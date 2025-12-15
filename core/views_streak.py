"""
Login streak system for user retention.
"""
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WalletTransaction


class LoginStreakView(APIView):
    """
    Track and reward daily login streaks.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Record a login and update streak.
        Called when user logs in or visits dashboard.
        """
        user = request.user
        today = timezone.now().date()

        # If no last login date, start streak
        if not user.last_login_date:
            user.login_streak = 1
            user.last_login_date = today
            user.longest_streak = max(user.longest_streak, 1)
            user.save(update_fields=["login_streak", "last_login_date", "longest_streak"])
            return Response({
                "streak": 1,
                "message": "Streak started!",
                "bonus": 0
            })

        # If already logged in today, return current streak
        if user.last_login_date == today:
            return Response({
                "streak": user.login_streak,
                "message": "Already logged in today",
                "bonus": 0
            })

        # Calculate days since last login
        days_diff = (today - user.last_login_date).days

        if days_diff == 1:
            # Consecutive day - increase streak
            user.login_streak += 1
            user.last_login_date = today
            user.longest_streak = max(user.longest_streak, user.login_streak)
            
            # Streak bonus (increasing with streak length)
            streak_bonus = min(user.login_streak * 2, 50)  # Max 50 coins
            
            user.coins_balance += streak_bonus
            user.save(update_fields=["login_streak", "last_login_date", "longest_streak", "coins_balance"])

            # Record transaction
            WalletTransaction.objects.create(
                user=user,
                type="bonus",
                coins=streak_bonus,
                note=f"Login streak bonus ({user.login_streak} days)"
            )

            return Response({
                "streak": user.login_streak,
                "message": f"🔥 {user.login_streak} day streak!",
                "bonus": streak_bonus,
                "new_balance": user.coins_balance
            })
        else:
            # Streak broken - reset to 1
            user.login_streak = 1
            user.last_login_date = today
            user.save(update_fields=["login_streak", "last_login_date"])

            return Response({
                "streak": 1,
                "message": "Streak reset. Start a new one!",
                "bonus": 0
            })

    def get(self, request):
        """Get current streak status."""
        user = request.user
        today = timezone.now().date()
        
        # Check if streak is still active
        if user.last_login_date == today:
            is_active = True
        elif user.last_login_date and (today - user.last_login_date).days == 1:
            is_active = True  # Can still continue today
        else:
            is_active = False

        return Response({
            "current_streak": user.login_streak,
            "longest_streak": user.longest_streak,
            "last_login": user.last_login_date.isoformat() if user.last_login_date else None,
            "is_active": is_active
        })

