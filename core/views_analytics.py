"""
User analytics and statistics endpoints.
"""
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import timedelta
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserTask, WalletTransaction, Task


class UserAnalyticsView(APIView):
    """
    Get comprehensive user analytics including:
    - Earnings overview (total, today, this week, this month)
    - Task completion stats
    - Withdrawal history
    - Referral stats
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        # Earnings Overview
        total_earned = WalletTransaction.objects.filter(
            user=user,
            type__in=["earn", "bonus", "referral"]
        ).aggregate(total=Sum("coins"))["total"] or 0

        today_earned = WalletTransaction.objects.filter(
            user=user,
            type__in=["earn", "bonus", "referral"],
            created_at__date=today
        ).aggregate(total=Sum("coins"))["total"] or 0

        week_earned = WalletTransaction.objects.filter(
            user=user,
            type__in=["earn", "bonus", "referral"],
            created_at__date__gte=week_ago
        ).aggregate(total=Sum("coins"))["total"] or 0

        month_earned = WalletTransaction.objects.filter(
            user=user,
            type__in=["earn", "bonus", "referral"],
            created_at__date__gte=month_ago
        ).aggregate(total=Sum("coins"))["total"] or 0

        # Task Statistics
        total_tasks = UserTask.objects.filter(user=user, status="completed").count()
        today_tasks = UserTask.objects.filter(
            user=user,
            status="completed",
            completed_at__date=today
        ).count()
        week_tasks = UserTask.objects.filter(
            user=user,
            status="completed",
            completed_at__date__gte=week_ago
        ).count()

        # Task type breakdown
        task_types = UserTask.objects.filter(
            user=user,
            status="completed"
        ).values("task__type").annotate(count=Count("id"))

        # Withdrawal Stats
        total_withdrawn = WalletTransaction.objects.filter(
            user=user,
            type="withdraw"
        ).aggregate(total=Sum("amount_rs"))["total"] or 0

        pending_withdrawals = user.withdrawals.filter(status="pending").count()

        # Referral Stats
        total_referrals = user.referrals.count()
        active_referrals = user.referrals.filter(
            last_earn_date__gte=week_ago
        ).count()

        # Average earnings per day (last 7 days)
        daily_earnings = []
        for i in range(7):
            date = today - timedelta(days=i)
            day_earned = WalletTransaction.objects.filter(
                user=user,
                type__in=["earn", "bonus", "referral"],
                created_at__date=date
            ).aggregate(total=Sum("coins"))["total"] or 0
            daily_earnings.append({
                "date": date.isoformat(),
                "coins": day_earned
            })

        return Response({
            "earnings": {
                "total": total_earned,
                "today": today_earned,
                "this_week": week_earned,
                "this_month": month_earned,
                "daily_breakdown": daily_earnings
            },
            "tasks": {
                "total_completed": total_tasks,
                "today": today_tasks,
                "this_week": week_tasks,
                "by_type": list(task_types)
            },
            "withdrawals": {
                "total_rs": float(total_withdrawn),
                "pending_count": pending_withdrawals
            },
            "referrals": {
                "total": total_referrals,
                "active": active_referrals
            },
            "user_level": user.user_level,
            "total_experience": user.total_experience,
            "login_streak": user.login_streak,
            "longest_streak": user.longest_streak
        }, status=status.HTTP_200_OK)

