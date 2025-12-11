from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    MeView,
    TaskListView,
    TaskStartView,
    TaskCompleteView,
    WalletView,
    WithdrawRequestView,
    UserWithdrawListView,
)
from .views_daily_bonus import DailyBonusView
from .views_referrals import ReferralAnalyticsView
from .views_daily_bonus import DailyBonusView



urlpatterns = [
    # Auth
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),

    # User profile
    path("me/", MeView.as_view(), name="me"),

    # Tasks / earning
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/start/<int:task_id>/", TaskStartView.as_view(), name="task_start"),
    path(
        "tasks/complete/<int:user_task_id>/",
        TaskCompleteView.as_view(),
        name="task_complete",
    ),

    # Wallet & withdraw
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("withdraw/", WithdrawRequestView.as_view(), name="withdraw_request"),
    path("withdraws/", UserWithdrawListView.as_view(), name="withdraw_list"),

    # NEW: daily bonus
    path("daily-bonus/", DailyBonusView.as_view(), name="daily_bonus"),

    # NEW: referral analytics for the logged-in user
    path("referrals/", ReferralAnalyticsView.as_view(), name="referrals"),
]
