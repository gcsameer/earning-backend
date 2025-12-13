from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import (
    User,
    Settings,
    Task,
    UserTask,
    WalletTransaction,
    WithdrawRequest,
    FraudEvent,
    CPXTransaction,
)


# -----------------------------------------
# USER ADMIN
# -----------------------------------------
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Extra Info",
            {
                "fields": (
                    "phone",
                    "ref_code",
                    "referred_by",
                    "device_id",
                    "fraud_score",
                    "coins_balance",
                    "last_earn_time",
                    "daily_earn_count",
                    "last_earn_date",
                    "daily_bonus_claimed",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "phone",
        "coins_balance",
        "fraud_score",
        "daily_earn_count",
    )

    search_fields = ("username", "email", "phone")
    raw_id_fields = ("referred_by",)  # prevents huge dropdowns


# -----------------------------------------
# SETTINGS ADMIN
# -----------------------------------------
@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "value")
    search_fields = ("key",)


# -----------------------------------------
# TASKS ADMIN
# -----------------------------------------
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "reward_coins", "is_active", "created_at")
    list_filter = ("type", "is_active")
    search_fields = ("title",)


# -----------------------------------------
# USER TASK ADMIN
# -----------------------------------------
@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "status", "started_at", "completed_at")
    list_filter = ("status",)
    search_fields = ("user__username", "task__title")
    list_select_related = ("user", "task")


# -----------------------------------------
# WALLET TRANSACTIONS
# -----------------------------------------
@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "coins", "amount_rs", "created_at")
    list_filter = ("type",)
    search_fields = ("user__username",)
    list_select_related = ("user",)


# -----------------------------------------
# WITHDRAW REQUESTS ADMIN
# -----------------------------------------
@admin.register(WithdrawRequest)
class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "amount_rs", "method", "account_id", "status", "created_at")
    list_filter = ("method", "status")
    search_fields = ("user__username", "account_id")
    list_select_related = ("user",)


# -----------------------------------------
# FRAUD EVENT ADMIN
# -----------------------------------------
@admin.register(FraudEvent)
class FraudEventAdmin(admin.ModelAdmin):
    list_display = ("user", "event_type", "score", "created_at")
    list_filter = ("event_type",)
    search_fields = ("user__username", "reason")
    list_select_related = ("user",)


# -----------------------------------------
# CPX TRANSACTION ADMIN
# -----------------------------------------
@admin.register(CPXTransaction)
class CPXTransactionAdmin(admin.ModelAdmin):
    list_display = ("trans_id", "user", "event", "status", "amount_local", "applied", "created_at")
    list_filter = ("event", "status", "applied")
    search_fields = ("trans_id", "user__username")
    list_select_related = ("user",)
    readonly_fields = ("trans_id", "created_at")
