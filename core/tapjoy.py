"""
Tapjoy Integration
- Offerwall for web and mobile
- Postback handler for rewards
"""
import os
import hashlib
import hmac
from urllib.parse import urlencode

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import TapjoyTransaction, WalletTransaction


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def build_tapjoy_wall_url(user):
    """
    Build Tapjoy offerwall URL for web.
    For mobile, use Tapjoy SDK directly.
    """
    sdk_key = _get_env("TAPJOY_SDK_KEY")
    user_id = str(user.id)  # Stable unique user ID
    
    if not sdk_key:
        return None, "TAPJOY_SDK_KEY missing"
    
    # Tapjoy web offerwall URL
    # Note: Tapjoy primarily uses SDK for mobile, but web can use direct links
    # For web, we'll use Tapjoy's web SDK or direct offerwall link
    base = "https://www.tapjoy.com/offers"
    
    params = {
        "sdk_key": sdk_key,
        "user_id": user_id,
    }
    
    return f"{base}?{urlencode(params)}", None


def verify_tapjoy_signature(secret_key: str, payload: str, signature: str) -> bool:
    """Verify Tapjoy postback signature"""
    if not secret_key or not signature:
        return False
    
    expected = hmac.new(
        secret_key.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tapjoy_wall_url(request):
    """Get Tapjoy offerwall URL for web"""
    url, err = build_tapjoy_wall_url(request.user)
    if err:
        return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        "url": url,
        "sdk_key": _get_env("TAPJOY_SDK_KEY"),
        "user_id": str(request.user.id),
    })


@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def tapjoy_postback(request):
    """
    Tapjoy postback handler.
    Tapjoy sends rewards via POST with JSON or GET with query params.
    
    Expected fields:
    - user_id: Tapjoy user ID (maps to our user.id)
    - currency: Amount of currency earned
    - transaction_id: Unique transaction ID
    - signature: HMAC signature for verification (optional but recommended)
    """
    # Handle both POST (JSON) and GET (query params)
    if request.method == "POST":
        data = request.data if hasattr(request, 'data') else {}
        user_id = data.get("user_id") or data.get("user_id")
        currency = data.get("currency") or data.get("amount") or "0"
        transaction_id = data.get("transaction_id") or data.get("trans_id")
        signature = data.get("signature", "")
    else:
        user_id = request.query_params.get("user_id")
        currency = request.query_params.get("currency") or request.query_params.get("amount") or "0"
        transaction_id = request.query_params.get("transaction_id") or request.query_params.get("trans_id")
        signature = request.query_params.get("signature", "")
    
    if not transaction_id or not user_id:
        return Response(
            {"detail": "missing transaction_id or user_id"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify signature if secret key is provided
    secret_key = _get_env("TAPJOY_SECRET_KEY")
    if secret_key and signature:
        # Get raw body for signature verification
        raw_body = request.body.decode('utf-8') if hasattr(request, 'body') else ""
        if not verify_tapjoy_signature(secret_key, raw_body, signature):
            return Response(
                {"detail": "invalid signature"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    # Map Tapjoy user_id to our user
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return Response(
            {"detail": "invalid user_id"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user = User.objects.get(id=user_id_int)
    except User.DoesNotExist:
        return Response(
            {"detail": "user not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Parse currency amount (coins)
    try:
        coins = int(float(currency))
    except (ValueError, TypeError):
        coins = 0
    
    if coins <= 0:
        return Response({"ok": True, "message": "zero or negative amount"})
    
    # Idempotency: only apply a transaction once
    tx, created = TapjoyTransaction.objects.get_or_create(
        transaction_id=transaction_id,
        defaults={
            "user": user,
            "currency_amount": coins,
            "applied": False,
        },
    )
    
    if not created:
        # Already processed
        return Response({"ok": True, "duplicate": True})
    
    # Apply reward
    user.coins_balance += coins
    user.save(update_fields=["coins_balance"])
    
    WalletTransaction.objects.create(
        user=user,
        type="earn",
        coins=coins,
        amount_rs=0,
        note=f"Tapjoy offerwall (transaction_id={transaction_id})",
    )
    
    tx.applied = True
    tx.save(update_fields=["applied"])
    
    return Response({"ok": True, "coins_added": coins})

