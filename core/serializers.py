from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    Task,
    WalletTransaction,
    WithdrawRequest,
)

User = get_user_model()


# -----------------------------------------------------------
# REGISTER SERIALIZER
# -----------------------------------------------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "password",
            "confirm_password",
            "referral_code",
        )

    def validate(self, attrs):
        pwd = attrs.get("password")
        confirm = attrs.pop("confirm_password", None)

        if pwd != confirm:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):
        referral_code = validated_data.pop("referral_code", "").strip().upper()
        password = validated_data.pop("password")

        # CREATE USER
        user = User(**validated_data)
        user.set_password(password)

        # generate referral code if missing
        if not user.ref_code:
            import random, string
            user.ref_code = "".join(random.choices(
                string.ascii_uppercase + string.digits, k=8
            ))

        # APPLY REFERRAL ONLY IF VALID
        if referral_code and referral_code != user.ref_code:
            try:
                referrer = User.objects.get(ref_code=referral_code)
                user.referred_by = referrer
            except User.DoesNotExist:
                pass

        user.save()

        # APPLY REFERRAL BONUS (AFTER SAVE)
        if user.referred_by:
            referrer_bonus = 50
            user_bonus = 20

            user.referred_by.coins_balance += referrer_bonus
            user.referred_by.save(update_fields=["coins_balance"])

            WalletTransaction.objects.create(
                user=user.referred_by,
                type="referral",
                coins=referrer_bonus,
                note=f"Referral bonus for inviting {user.username}",
            )

            user.coins_balance += user_bonus
            user.save(update_fields=["coins_balance"])

            WalletTransaction.objects.create(
                user=user,
                type="bonus",
                coins=user_bonus,
                note="Signup referral bonus",
            )

        return user


# -----------------------------------------------------------
# USER SERIALIZER
# -----------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone",
            "ref_code",
            "coins_balance",
            "fraud_score",
            "login_streak",
            "longest_streak",
            "user_level",
            "total_experience",
        )


# -----------------------------------------------------------
# TASK SERIALIZER
# -----------------------------------------------------------

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "type",
            "title",
            "description",
            "reward_coins",
            "ad_network",
            "ad_placement_id",
        )


# -----------------------------------------------------------
# WALLET SERIALIZER
# -----------------------------------------------------------

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = (
            "id",
            "type",
            "coins",
            "amount_rs",
            "note",
            "created_at",
        )


# -----------------------------------------------------------
# WITHDRAW SERIALIZER
# -----------------------------------------------------------

class WithdrawRequestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = WithdrawRequest
        fields = [
            "id",
            "user",
            "username",
            "user_email",
            "amount_rs",
            "method",
            "account_id",
            "status",
            "admin_note",
            "created_at",
            "processed_at",
        ]
        read_only_fields = ["status", "admin_note", "created_at", "processed_at", "user"]
    
    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
            "phone": obj.user.phone,
        }

    def validate_amount_rs(self, value):
        """Ensure withdraw amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return WithdrawRequest.objects.create(user=user, **validated_data)


# -----------------------------------------------------------
# REFERRAL ANALYTICS SERIALIZER
# -----------------------------------------------------------

class ReferralUserSummarySerializer(serializers.ModelSerializer):
    """Used by ReferralAnalyticsView to show invited user's progress."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "coins_balance",
            "fraud_score",
        ]
