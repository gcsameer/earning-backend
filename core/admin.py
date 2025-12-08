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
)


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
                )
            },
        ),
    )
    list_display = ("username", "email", "phone", "coins_balance", "fraud_score")
    search_fields = ("username", "email", "phone")


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "value")
    search_fields = ("key",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "reward_coins", "is_active", "created_at")
    list_filter = ("type", "is_active")
    search_fields = ("title",)


@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "status", "started_at", "completed_at")
    list_filter = ("status",)
    search_fields = ("user__username", "task__title")


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "coins", "amount_rs", "created_at")
    list_filter = ("type",)
    search_fields = ("user__username",)


@admin.register(WithdrawRequest)
class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "amount_rs", "method", "account_id", "status", "created_at")
    list_filter = ("method", "status")
    search_fields = ("user__username", "account_id")


@admin.register(FraudEvent)
class FraudEventAdmin(admin.ModelAdmin):
    list_display = ("user", "event_type", "score", "created_at")
    list_filter = ("event_type",)
    search_fields = ("user__username", "reason")
