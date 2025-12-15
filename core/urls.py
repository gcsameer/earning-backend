from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .cpx import cpx_wall_url, cpx_postback

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
    RewardedAdCompleteView,
)
from .views_email_verification import EmailVerificationView

from .views_daily_bonus import DailyBonusView
from .views_referrals import ReferralAnalyticsView
from .views_games import GameTaskCompleteView
from .views_cors_test import CORSTestView
from .views_analytics import UserAnalyticsView
from .views_streak import LoginStreakView
from .views_achievements import AchievementsView
from .views_challenges import DailyChallengesView
from .views_admin import AdminWithdrawListView, AdminWithdrawDetailView, AdminWithdrawActionView, AdminWithdrawActionView


urlpatterns = [

    # -------------------------
    # AUTH
    # -------------------------
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/verify-email/", EmailVerificationView.as_view(), name="verify_email"),

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
    # Game-based tasks (instant completion)
    path("tasks/game/complete/<int:task_id>/", GameTaskCompleteView.as_view(), name="game_task_complete"),

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
    
    # -------------------------
    # ANALYTICS & STATS
    # -------------------------
    path("analytics/", UserAnalyticsView.as_view(), name="user_analytics"),
    
    # -------------------------
    # LOGIN STREAK
    # -------------------------
    path("streak/", LoginStreakView.as_view(), name="login_streak"),
    
    # -------------------------
    # ACHIEVEMENTS
    # -------------------------
    path("achievements/", AchievementsView.as_view(), name="achievements"),
    
    # -------------------------
    # DAILY CHALLENGES
    # -------------------------
    path("challenges/", DailyChallengesView.as_view(), name="daily_challenges"),
    
    # -------------------------
    # CORS TEST (for debugging)
    # -------------------------
    path("cors-test/", CORSTestView.as_view(), name="cors_test"),
    
    # -------------------------
    # ADS
    # -------------------------
    path("ads/rewarded/complete/", RewardedAdCompleteView.as_view(), name="rewarded_ad_complete"),
    
    # -------------------------
    # CPX
    # -------------------------
    path("cpx/wall/", cpx_wall_url, name="cpx_wall"),
    path("cpx/postback/", cpx_postback, name="cpx_postback"),
    
    # -------------------------
    # ADMIN (Admin only - requires IsAdminUser permission)
    # -------------------------
    path("admin/withdraws/", AdminWithdrawListView.as_view(), name="admin_withdraw_list"),
    path("admin/withdraws/<int:withdraw_id>/", AdminWithdrawDetailView.as_view(), name="admin_withdraw_detail"),
    path("admin/withdraws/<int:withdraw_id>/<str:action>/", AdminWithdrawActionView.as_view(), name="admin_withdraw_action"),
]
