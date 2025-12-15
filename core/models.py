from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
import string
import random


# -----------------------------------------
# USER MODEL
# -----------------------------------------
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)

    # Referral system
    ref_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="referrals",
    )

    # Device / anti-fraud
    device_id = models.CharField(max_length=255, blank=True, null=True, default="")

    fraud_score = models.FloatField(default=0.0)

    # Wallet
    coins_balance = models.IntegerField(default=0)

    # Earning limits
    last_earn_time = models.DateTimeField(null=True, blank=True)
    daily_earn_count = models.IntegerField(default=0)
    last_earn_date = models.DateField(null=True, blank=True)
    daily_bonus_claimed = models.DateField(null=True, blank=True)
    
    # Login streak system
    login_streak = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)
    longest_streak = models.IntegerField(default=0)
    
    # User level/experience
    user_level = models.IntegerField(default=1)
    total_experience = models.IntegerField(default=0)

    # ------------------------------
    # AUTO-GENERATE REFERRAL CODE
    # ------------------------------
    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        super().save(*args, **kwargs)

    # ------------------------------
    # DAILY EARNING LIMIT CHECK
    # ------------------------------
    def can_earn_now(self, max_per_day=100):
        today = timezone.now().date()
        if self.last_earn_date != today:
            return True
        return self.daily_earn_count < max_per_day

    # ------------------------------
    # REGISTER EARNING EVENT
    # ------------------------------
    def register_earn(self):
        now = timezone.now()
        today = now.date()

        if self.last_earn_date != today:
            self.last_earn_date = today
            self.daily_earn_count = 1
        else:
            self.daily_earn_count += 1

        self.last_earn_time = now
        self.save(
            update_fields=["last_earn_date", "daily_earn_count", "last_earn_time"]
        )


# -----------------------------------------
# SETTINGS MODEL
# -----------------------------------------
class Settings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key} = {self.value}"

    @staticmethod
    def get_value(key: str, default=None):
        try:
            return Settings.objects.get(key=key).value
        except Settings.DoesNotExist:
            return default


# -----------------------------------------
# TASK MODEL
# -----------------------------------------
class Task(models.Model):
    TASK_TYPES = (
        ("video", "Video"),
        ("quiz", "Quiz"),
        ("offerwall", "Offerwall"),
        ("tapjoy_offerwall", "Tapjoy Offerwall"),
        ("scratch_card", "Scratch Card"),
        ("spin_wheel", "Spin Wheel"),
        ("puzzle", "Puzzle"),
    )

    type = models.CharField(max_length=20, choices=TASK_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reward_coins = models.PositiveIntegerField(default=0)
    ad_network = models.CharField(max_length=50, blank=True)
    ad_placement_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------------------------------
# USER TASK MODEL
# -----------------------------------------
class UserTask(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_tasks"
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="user_tasks"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_id = models.CharField(max_length=255, blank=True, null=True, default="")


    def __str__(self):
        return f"{self.user} - {self.task} ({self.status})"


# -----------------------------------------
# WALLET TRANSACTION MODEL
# -----------------------------------------
class WalletTransaction(models.Model):
    TYPE_CHOICES = (
        ("earn", "Earn"),
        ("withdraw", "Withdraw"),
        ("bonus", "Bonus"),
        ("referral", "Referral"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wallet_transactions"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    coins = models.IntegerField()
    amount_rs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.type} - {self.coins} coins"


# -----------------------------------------
# WITHDRAW REQUEST MODEL
# -----------------------------------------
class WithdrawRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_PAID = "paid"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_PAID, "Paid"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="withdrawals",
    )
    amount_rs = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    account_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_rs} - {self.status}"


# -----------------------------------------
# FRAUD EVENT MODEL
# -----------------------------------------
class FraudEvent(models.Model):
    EVENT_TYPES = (
        ("suspicious_speed", "Suspicious task speed"),
        ("limit_exceeded", "Daily limit exceeded"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fraud_events"
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    score = models.FloatField(default=0.0)
    reason = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_id = models.CharField(max_length=255, blank=True, null=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event_type} ({self.score})"
    

class CPXTransaction(models.Model):

    trans_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.CharField(max_length=20, default="complete")  # complete|out|bonus|cancel
    status = models.IntegerField(default=1)  # 1 or 2
    amount_local = models.IntegerField(default=0)  # coins
    applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trans_id} ({self.user})"


class TapjoyTransaction(models.Model):
    """Tapjoy offerwall transaction tracking"""
    transaction_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency_amount = models.IntegerField(default=0)  # coins earned
    applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} ({self.user}) - {self.currency_amount} coins"
