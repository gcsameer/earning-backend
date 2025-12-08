from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, WalletTransaction, WithdrawRequest

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

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
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password", None)

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        referral_code = validated_data.pop("referral_code", "").strip()
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)

        # generate ref_code if missing
        if not user.ref_code:
            import random
            import string

            user.ref_code = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )

        # referred_by
        if referral_code:
            try:
                referrer = User.objects.get(ref_code=referral_code)
                user.referred_by = referrer
            except User.DoesNotExist:
                pass

        user.save()

        # referral bonuses
        if user.referred_by:
            referrer_bonus = 50
            user_bonus = 20

            user.referred_by.coins_balance += referrer_bonus
            user.referred_by.save()
            WalletTransaction.objects.create(
                user=user.referred_by,
                type="referral",
                coins=referrer_bonus,
                note=f"Referral bonus for inviting {user.username}",
            )

            user.coins_balance += user_bonus
            user.save()
            WalletTransaction.objects.create(
                user=user,
                type="bonus",
                coins=user_bonus,
                note="Signup referral bonus",
            )

        return user


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
        )


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


class WithdrawRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = (
            "id",
            "amount_rs",
            "method",
            "account_id",
            "status",
            "created_at",
        )
        read_only_fields = ("status", "created_at")
