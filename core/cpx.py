# core/cpx.py
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone

from .models import User, WalletTransaction, CPXTransaction


def _get_user_from_ext_user_id(ext_user_id: str) -> User | None:
    """
    ext_user_id is whatever you send to CPX as &ext_user_id=...
    Support both:
      - numeric user.id
      - username
    """
    if not ext_user_id:
        return None

    # numeric = user.id
    if ext_user_id.isdigit():
        return User.objects.filter(id=int(ext_user_id)).first()

    # otherwise = username
    return User.objects.filter(username=ext_user_id).first()


def cpx_wall_url(request):
    """
    Build offerwall URL.
    You should pass a stable identifier as ext_user_id.
    Recommended: user.id (numeric).
    Example: /api/cpx/wall/?user_id=12
    """
    user_id = request.GET.get("user_id")
    if not user_id:
        return HttpResponseBadRequest("Missing user_id")

    app_id = getattr(settings, "CPX_APP_ID", None)
    if not app_id:
        return HttpResponseBadRequest("Missing CPX_APP_ID in settings")

    # You can also add &secure_hash=... if CPX enabled hashing for your account.
    url = f"https://offers.cpx-research.com/index.php?app_id={app_id}&ext_user_id={user_id}"
    return JsonResponse({"url": url})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def cpx_postback(request):
    """
    CPX Postback endpoint.
    - Idempotent: same trans_id won't pay twice
    - Writes WalletTransaction
    - Updates User.coins_balance
    - Marks CPXTransaction.applied=True once paid

    IMPORTANT:
    - If CPX provides secure_hash verification, you MUST verify it here according to CPX docs.
      (I am not guessing the hash formula, because using the wrong one can break payouts.)
    """

    data = request.GET if request.method == "GET" else request.POST

    # CPX commonly sends these (names can vary slightly)
    trans_id = (data.get("trans_id") or "").strip()
    ext_user_id = (data.get("user_id") or data.get("ext_user_id") or "").strip()
    event = (data.get("event") or "complete").strip().lower()  # complete|out|bonus|cancel...
    status_raw = (data.get("status") or "1").strip()

    amount_local_raw = (data.get("amount_local") or "0").strip()  # coins in your system
    amount_usd_raw = (data.get("amount_usd") or "0").strip()

    secure_hash = (data.get("secure_hash") or "").strip()

    if not trans_id or not ext_user_id:
        return HttpResponseBadRequest("Missing trans_id or user_id/ext_user_id")

    # --- OPTIONAL: secure_hash verification gate (turn on when CPX gives you the exact formula)
    # If you want to enforce it, set CPX_REQUIRE_SECURE_HASH=True in settings,
    # and implement verify function below exactly as per CPX docs.
    require_hash = getattr(settings, "CPX_REQUIRE_SECURE_HASH", False)
    if require_hash and not secure_hash:
        return HttpResponse("missing_secure_hash", status=403)

    # ---- parse numeric fields safely
    try:
        status = int(status_raw)
    except ValueError:
        status = 1

    try:
        amount_local = int(Decimal(amount_local_raw))
    except (InvalidOperation, ValueError):
        amount_local = 0

    # We store USD just for logging
    try:
        amount_usd = Decimal(amount_usd_raw)
    except (InvalidOperation, ValueError):
        amount_usd = Decimal("0")

    user = _get_user_from_ext_user_id(ext_user_id)
    if not user:
        return HttpResponse("unknown_user", status=404)

    # Decide whether this event should reward user
    # - "complete" => reward
    # - "bonus" => reward
    # - "out" (screen-out) => you can reward small bonus if you want
    # - "cancel" => no reward
    rewardable_events = {"complete", "bonus", "out"}
    if event not in rewardable_events:
        # still record transaction as not applied (optional)
        CPXTransaction.objects.get_or_create(
            trans_id=trans_id,
            defaults={
                "user": user,
                "event": event[:20],
                "status": status,
                "amount_local": 0,
                "applied": False,
            },
        )
        return HttpResponse("ok", status=200)

    # If amount_local is 0 for out/bonus, you can give a fixed minimal bonus
    if amount_local <= 0:
        # keep small to avoid abuse; adjust as you like
        if event == "out":
            amount_local = 5
        elif event == "bonus":
            amount_local = 10
        else:
            amount_local = 0

    # No money -> no coins
    if amount_local <= 0:
        CPXTransaction.objects.get_or_create(
            trans_id=trans_id,
            defaults={
                "user": user,
                "event": event[:20],
                "status": status,
                "amount_local": 0,
                "applied": False,
            },
        )
        return HttpResponse("ok", status=200)

    # --- Idempotent apply
    with transaction.atomic():
        tx, created = CPXTransaction.objects.select_for_update().get_or_create(
            trans_id=trans_id,
            defaults={
                "user": user,
                "event": event[:20],
                "status": status,
                "amount_local": amount_local,
                "applied": False,
            },
        )

        # If already applied, do nothing (prevents double payment)
        if tx.applied:
            return HttpResponse("ok", status=200)

        # If transaction exists but amount differs, keep the first one (safer)
        if not created:
            tx.event = event[:20]
            tx.status = status
            if tx.amount_local <= 0:
                tx.amount_local = amount_local
            tx.save(update_fields=["event", "status", "amount_local"])

        # Apply coins
        user.coins_balance += int(tx.amount_local)
        user.last_earn_time = timezone.now()
        user.save(update_fields=["coins_balance", "last_earn_time"])

        # Wallet history
        WalletTransaction.objects.create(
            user=user,
            type="bonus" if event == "bonus" else "earn",
            coins=int(tx.amount_local),
            amount_rs=Decimal("0"),
            note=f"CPX {event} | trans_id={tx.trans_id} | usd={amount_usd}",
        )

        tx.applied = True
        tx.save(update_fields=["applied"])

    # CPX usually accepts plain "ok"
    return HttpResponse("ok", status=200)
