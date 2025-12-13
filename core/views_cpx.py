import hashlib
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction

from django.contrib.auth import get_user_model

User = get_user_model()


def _md5(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def _verify_cpx_hash(user_id: str, secure_hash_from_cpx: str) -> bool:
    # CPX formula: md5(ext_user_id + "-" + your_secure_hash)
    expected = _md5(f"{user_id}-{settings.CPX_SECURITY_HASH}")
    return secure_hash_from_cpx == expected


@csrf_exempt
@require_http_methods(["GET"])
def cpx_postback(request):
    """
    CPX calls this URL server-to-server.
    Example params:
      event=out|bonus|cancel (we add)
      status=1|2
      trans_id=...
      user_id=...
      amount_local=...
      amount_usd=...
      secure_hash=...
    """

    user_id = request.GET.get("user_id", "")
    trans_id = request.GET.get("trans_id", "")
    status = request.GET.get("status", "")  # 1=completed, 2=cancelled/reversal
    event = request.GET.get("event", "complete")
    amount_local = request.GET.get("amount_local", "0")
    secure_hash = request.GET.get("secure_hash", "")

    if not (user_id and trans_id and status and secure_hash):
        return HttpResponseBadRequest("Missing required parameters")

    if not settings.CPX_SECURITY_HASH:
        return HttpResponseBadRequest("Server missing CPX_SECURITY_HASH")

    if not _verify_cpx_hash(user_id, secure_hash):
        return HttpResponseBadRequest("Invalid secure_hash")

    # parse coins safely
    try:
        coins = int(Decimal(amount_local))
    except Exception:
        return HttpResponseBadRequest("Invalid amount_local")

    # Find your user by username (since your frontend uses username)
    try:
        user = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("Unknown user_id")

    # IMPORTANT:
    # Prevent double-credit if CPX retries the same trans_id.
    # If you already have a model/table for transactions, check it here.
    # Below is a minimal safe approach: store trans_id in a user profile field/table.
    # If you don't have it yet, create a model (recommended).
    from core.models import CPXTransaction  # create model below

    with transaction.atomic():
        tx, created = CPXTransaction.objects.get_or_create(
            trans_id=trans_id,
            defaults={
                "user": user,
                "event": event,
                "status": int(status),
                "amount_local": coins,
            },
        )

        if not created:
            # already processed
            return JsonResponse({"ok": True, "duplicate": True})

        # Status 1 = credit, Status 2 = reversal (deduct)
        # CPX recommends status param usage for reversals. 
        if int(status) == 1:
            user.coins_balance += coins
            user.save(update_fields=["coins_balance"])
            tx.applied = True
            tx.save(update_fields=["applied"])
            return JsonResponse({"ok": True, "credited": coins, "event": event})

        if int(status) == 2:
            # reversal: deduct but don't go negative
            user.coins_balance = max(0, user.coins_balance - coins)
            user.save(update_fields=["coins_balance"])
            tx.applied = True
            tx.save(update_fields=["applied"])
            return JsonResponse({"ok": True, "reversed": coins, "event": event})

    return JsonResponse({"ok": True})
