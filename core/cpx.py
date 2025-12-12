import os
from urllib.parse import urlencode

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import CPXTransaction, WalletTransaction, Settings

User = get_user_model()


def cpx_wall_url(request):
    """
    Returns a CPX offerwall URL for the logged-in user.
    Frontend will open this in an iframe.
    """
    user = request.user
    app_id = os.environ.get("CPX_APP_ID", "")
    if not app_id:
        return JsonResponse({"detail": "CPX_APP_ID missing"}, status=500)

    # ext_user_id: IMPORTANT
    # Use a stable unique value. Best: user.id (integer). Do NOT change later.
    ext_user_id = str(user.id)

    # Optional: a token you set yourself (NOT CPX secret). Helps validate postbacks.
    postback_token = os.environ.get("CPX_POSTBACK_TOKEN", "")

    params = {
        "app_id": app_id,
        "ext_user_id": ext_user_id,
    }

    # If CPX allows custom params, we pass a token too (many offerwalls allow it).
    # If CPX ignores unknown params, it won't break anything.
    if postback_token:
        params["token"] = postback_token

    url = "https://offers.cpx-research.com/index.php?" + urlencode(params)
    return JsonResponse({"url": url})


@csrf_exempt
def cpx_postback(request):
    """
    CPX server-to-server callback.
    You will paste this URL in CPX Postback settings.

    We credit coins once per unique trans_id.
    """

    # CPX often sends these as query params
    trans_id = request.GET.get("trans_id") or request.POST.get("trans_id")
    ext_user_id = request.GET.get("ext_user_id") or request.POST.get("ext_user_id")
    amount_local = request.GET.get("amount_local") or request.POST.get("amount_local") or "0"
    status = request.GET.get("status") or request.POST.get("status") or "1"
    event = request.GET.get("event") or request.POST.get("event") or "complete"

    # Optional: our own token check (recommended)
    expected = os.environ.get("CPX_POSTBACK_TOKEN", "")
    got = request.GET.get("token") or request.POST.get("token") or ""
    if expected and got != expected:
        return JsonResponse({"detail": "invalid token"}, status=403)

    if not trans_id or not ext_user_id:
        return JsonResponse({"detail": "missing trans_id/ext_user_id"}, status=400)

    try:
        coins = int(float(amount_local))
    except Exception:
        coins = 0

    # Only credit on status=1 (completed). If CPX uses different codes, adjust here.
    try:
        status_int = int(status)
    except Exception:
        status_int = 1

    # Create transaction row (dedupe)
    obj, created = CPXTransaction.objects.get_or_create(
        trans_id=trans_id,
        defaults={
            "user_id": int(ext_user_id),
            "event": event,
            "status": status_int,
            "amount_local": coins,
            "applied": False,
        },
    )

    # If already exists, just return OK (prevents double-credit)
    if not created:
        return JsonResponse({"ok": True, "duplicate": True})

    # Only credit if status=1 and not applied
    if status_int != 1 or coins <= 0:
        return JsonResponse({"ok": True, "credited": False})

    # Credit user
    try:
        user = User.objects.get(id=int(ext_user_id))
    except User.DoesNotExist:
        return JsonResponse({"detail": "user not found"}, status=404)

    # Apply coins
    user.coins_balance += coins
    # also update daily counters if you want
    if hasattr(user, "register_earn"):
        user.register_earn()
    else:
        user.save(update_fields=["coins_balance"])

    WalletTransaction.objects.create(
        user=user,
        type="earn",
        coins=coins,
        note=f"CPX Offerwall reward (trans_id={trans_id})",
    )

    obj.user = user
    obj.applied = True
    obj.save(update_fields=["user", "applied"])

    return JsonResponse({"ok": True, "credited": True, "coins": coins})
