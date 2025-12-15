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
    list_display = ("user", "amount_rs", "method", "account_id", "status_badge", "created_at", "processed_at", "action_buttons")
    list_filter = ("method", "status", "created_at")
    search_fields = ("user__username", "user__email", "account_id")
    list_select_related = ("user",)
    readonly_fields = ("user", "amount_rs", "method", "account_id", "created_at")
    fieldsets = (
        ("Request Details", {
            "fields": ("user", "amount_rs", "method", "account_id", "status", "created_at")
        }),
        ("Admin Actions", {
            "fields": ("admin_note", "processed_at")
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            "pending": "warning",
            "approved": "info",
            "rejected": "danger",
            "paid": "success"
        }
        color = colors.get(obj.status, "secondary")
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = "status"
    
    def action_buttons(self, obj):
        if obj.status == "pending":
            return format_html(
                '<a href="/admin/core/withdrawrequest/{}/change/" class="btn btn-sm btn-success" style="margin-right: 5px;">Approve</a>'
                '<a href="/admin/core/withdrawrequest/{}/change/" class="btn btn-sm btn-danger">Reject</a>',
                obj.id, obj.id
            )
        return "-"
    action_buttons.short_description = "Actions"
    
    actions = ["approve_requests", "reject_requests", "mark_as_paid"]
    
    def approve_requests(self, request, queryset):
        """Approve selected withdrawal requests"""
        from django.utils import timezone
        updated = queryset.filter(status=WithdrawRequest.STATUS_PENDING).update(
            status=WithdrawRequest.STATUS_APPROVED,
            processed_at=timezone.now()
        )
        self.message_user(request, f"{updated} withdrawal request(s) approved.")
    approve_requests.short_description = "Approve selected requests"
    
    def reject_requests(self, request, queryset):
        """Reject selected withdrawal requests"""
        from django.utils import timezone
        from django.db import transaction
        
        updated = 0
        with transaction.atomic():
            for withdraw in queryset.filter(status=WithdrawRequest.STATUS_PENDING):
                # Refund coins to user
                rate = float(Settings.get_value("COIN_TO_RS_RATE", "0.1"))
                coins_to_refund = int(float(withdraw.amount_rs) / rate)
                withdraw.user.coins_balance += coins_to_refund
                withdraw.user.save(update_fields=["coins_balance"])
                
                # Update withdrawal status
                withdraw.status = WithdrawRequest.STATUS_REJECTED
                withdraw.processed_at = timezone.now()
                withdraw.save()
                updated += 1
        
        self.message_user(request, f"{updated} withdrawal request(s) rejected and coins refunded.")
    reject_requests.short_description = "Reject selected requests (refund coins)"
    
    def mark_as_paid(self, request, queryset):
        """Mark selected withdrawal requests as paid"""
        from django.utils import timezone
        updated = queryset.filter(status=WithdrawRequest.STATUS_APPROVED).update(
            status=WithdrawRequest.STATUS_PAID,
            processed_at=timezone.now()
        )
        self.message_user(request, f"{updated} withdrawal request(s) marked as paid.")
    mark_as_paid.short_description = "Mark as paid"


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
