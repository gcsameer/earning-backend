from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_cpx import cpx_postback
from core.views_cpx import cpx_postback

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


urlpatterns = [

    # -------------------------
    # AUTH
    # -------------------------
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),

    # -------------------------
    # USER PROFILE
    # -------------------------
    path("me/", MeView.as_view(), name="me"),

    # -------------------------
    # TASK SYSTEM
    # -------------------------
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/start/<int:task_id>/", TaskStartView.as_view(), name="task_start"),
    path(
        "tasks/complete/<int:user_task_id>/",
        TaskCompleteView.as_view(),
        name="task_complete",

    
    ),

    # -------------------------
    # WALLET + WITHDRAW
    # -------------------------
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("withdraw/", WithdrawRequestView.as_view(), name="withdraw_request"),
    path("withdraws/", UserWithdrawListView.as_view(), name="withdraw_list"),

    # -------------------------
    # DAILY BONUS
    # -------------------------
    path("daily-bonus/", DailyBonusView.as_view(), name="daily_bonus"),

    # -------------------------
    # REFERRAL ANALYTICS
    # -------------------------
    path("referrals/", ReferralAnalyticsView.as_view(), name="referrals"),
    path("cpx/postback/", cpx_postback),
]
