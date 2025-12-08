from django.urls import path
from .views_referrals import ReferralAnalyticsView
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

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("tasks/start/<int:task_id>/", TaskStartView.as_view(), name="task_start"),
    path("tasks/complete/<int:user_task_id>/", TaskCompleteView.as_view(), name="task_complete"),
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("withdraw/", WithdrawRequestView.as_view(), name="withdraw_request"),
    path("withdraws/", UserWithdrawListView.as_view(), name="withdraw_list"),


path("referrals/", ReferralAnalyticsView.as_view()),
path("daily-bonus/", DailyBonusView.as_view()),


]
