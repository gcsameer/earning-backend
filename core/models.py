from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings





class User(AbstractUser):
    # Basic profile / referral fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    ref_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="referrals",
    )
    device_id = models.CharField(max_length=255, blank=True, null=True)

    # Anti-fraud / scoring
    fraud_score = models.FloatField(default=0.0)

    # Wallet
    coins_balance = models.IntegerField(default=0)

    # Earning rate / daily limit
    last_earn_time = models.DateTimeField(null=True, blank=True)
    daily_earn_count = models.IntegerField(default=0)
    last_earn_date = models.DateField(null=True, blank=True)

    def can_earn_now(self, max_per_day=100):
        """
        Check if the user can still earn today.
        Resets the counter automatically when the day changes.
        """
        today = timezone.now().date()

        if self.last_earn_date != today:
            # New day → reset
            self.last_earn_date = today
            self.daily_earn_count = 0
            self.save(update_fields=["last_earn_date", "daily_earn_count"])

        return self.daily_earn_count < max_per_day

    def register_earn(self):
        """
        Update daily counters and last_earn_time when the user earns once.
        (Do NOT modify coins_balance here – that’s done in the view.)
        """
        now = timezone.now()
        today = now.date()

        if self.last_earn_date != today:
            # First earn of the day
            self.last_earn_date = today
            self.daily_earn_count = 1
        else:
            self.daily_earn_count += 1

        self.last_earn_time = now
        self.save(update_fields=["last_earn_date", "daily_earn_count", "last_earn_time"])

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


class Task(models.Model):
    TASK_TYPES = (
        ("video", "Video"),
        ("quiz", "Quiz"),
        ("offerwall", "Offerwall"),
    )

    type = models.CharField(max_length=20, choices=TASK_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reward_coins = models.PositiveIntegerField(default=0)
    ad_network = models.CharField(max_length=50, blank=True)  # e.g., 'admob'
    ad_placement_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserTask(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tasks")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="user_tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.task} ({self.status})"


class WalletTransaction(models.Model):
    TYPE_CHOICES = (
        ("earn", "Earn"),
        ("withdraw", "Withdraw"),
        ("bonus", "Bonus"),
        ("referral", "Referral"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet_transactions")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    coins = models.IntegerField()
    amount_rs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.type} - {self.coins} coins"


class WithdrawRequest(models.Model):
    """
    Matches the name used in your views + serializers (WithdrawRequest).
    """
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="withdrawals")
    amount_rs = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)  # e.g. "khalti", "esewa", "bank"
    account_id = models.CharField(max_length=100)  # phone / account number
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_rs} - {self.status}"


class FraudEvent(models.Model):
    EVENT_TYPES = (
        ("suspicious_speed", "Suspicious task speed"),
        ("limit_exceeded", "Daily limit exceeded"),
        ("other", "Other"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fraud_events")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    score = models.FloatField(default=0.0)
    reason = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event_type} ({self.score})"
