from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    ref_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="referrals"
    )
    device_id = models.CharField(max_length=255, null=True, blank=True)
    fraud_score = models.FloatField(default=0.0)
    coins_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.username or self.email or f"User {self.id}"


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
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    METHOD_CHOICES = (
        ("esewa", "eSewa"),
        ("khalti", "Khalti"),
        ("imepay", "IME Pay"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="withdraw_requests")
    amount_rs = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    account_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.amount_rs} ({self.status})"


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
