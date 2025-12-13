import os
from urllib.parse import urlencode

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import CPXTransaction, WalletTransaction


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def build_cpx_wall_url(user):
    """
    ext_user_id MUST be unique per user. Best = user.id (stable).
    """
    app_id = _get_env("CPX_APP_ID")
    secure_hash = _get_env("CPX_SECURITY_HASH")

    if not app_id:
        return None, "CPX_APP_ID missing"
    if not secure_hash:
        return None, "CPX_SECURITY_HASH missing"

    ext_user_id = str(user.id)  # ✅ stable unique id
    currency = _get_env("CPX_CURRENCY", "coins")

    # CPX offers URL (works for web iframe)
    base = "https://offers.cpx-research.com/index.php"

    params = {
        "app_id": app_id,
        "ext_user_id": ext_user_id,
        "secure_hash": secure_hash,
        "currency": currency,
    }

    return f"{base}?{urlencode(params)}", None


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cpx_wall_url(request):
    url, err = build_cpx_wall_url(request.user)
    if err:
        return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"url": url})


@api_view(["GET"])
@permission_classes([AllowAny])
def cpx_postback(request):
    """
    CPX will call your URL like:
    /api/cpx/postback/?trans_id=...&ext_user_id=...&amount=...&status=1&event=complete

    We:
    - Ensure trans_id is processed once
    - Credit coins to the user
    """
    trans_id = request.query_params.get("trans_id") or request.query_params.get("transaction_id")
    ext_user_id = request.query_params.get("ext_user_id")
    amount = request.query_params.get("amount") or "0"
    status_str = request.query_params.get("status") or "1"
    event = (request.query_params.get("event") or "complete").lower()

    if not trans_id or not ext_user_id:
        return Response({"detail": "missing trans_id or ext_user_id"}, status=400)

    try:
        user_id = int(ext_user_id)
    except ValueError:
        return Response({"detail": "invalid ext_user_id"}, status=400)

    User = settings.AUTH_USER_MODEL

    # Import your user model properly
    from django.contrib.auth import get_user_model
    U = get_user_model()

    try:
        user = U.objects.get(id=user_id)
    except U.DoesNotExist:
        return Response({"detail": "user not found"}, status=404)

    # Make sure amount is int coins
    try:
        coins = int(float(amount))
    except ValueError:
        coins = 0

    # Idempotency: only apply a transaction once
    tx, created = CPXTransaction.objects.get_or_create(
        trans_id=trans_id,
        defaults={
            "user": user,
            "event": event,
            "status": int(status_str),
            "amount_local": coins,
            "applied": False,
        },
    )

    if not created:
        # If already applied, just return OK (CPX may retry)
        return Response({"ok": True, "duplicate": True})

    # Apply only if status=1 and event is complete/bonus/out (you decide)
    if int(status_str) == 1 and coins > 0:
        user.coins_balance += coins
        user.save(update_fields=["coins_balance"])

        WalletTransaction.objects.create(
            user=user,
            type="earn",
            coins=coins,
            amount_rs=0,
            note=f"CPX {event} (trans_id={trans_id})",
        )

        tx.applied = True
        tx.save(update_fields=["applied"])

    return Response({"ok": True})
