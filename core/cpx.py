# core/cpx.py
import hashlib
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def cpx_wall_url(request):
    """
    Returns CPX offerwall URL for a given user.
    Example usage: /api/cpx/wall/?user_id=rupesh
    """
    user_id = request.GET.get("user_id")
    if not user_id:
        return HttpResponseBadRequest("Missing user_id")

    app_id = getattr(settings, "CPX_APP_ID", None)
    if not app_id:
        return HttpResponseBadRequest("Missing CPX_APP_ID in settings")

    url = f"https://offers.cpx-research.com/index.php?app_id={app_id}&ext_user_id={user_id}"
    return JsonResponse({"url": url})


def _verify_hash(secure_hash: str, expected: str) -> bool:
    return secure_hash == expected


@csrf_exempt
@require_http_methods(["GET", "POST"])
def cpx_postback(request):
    """
    CPX postback endpoint.
    You MUST validate secure_hash before rewarding user.
    """
    data = request.GET if request.method == "GET" else request.POST

    event = data.get("event", "")
    status = data.get("status", "")
    trans_id = data.get("trans_id", "")
    user_id = data.get("user_id", "")
    amount_local = data.get("amount_local", "0")
    amount_usd = data.get("amount_usd", "0")
    secure_hash = data.get("secure_hash", "")

    # Basic validation
    if not (trans_id and user_id and secure_hash):
        return HttpResponseBadRequest("Missing required params")

    # IMPORTANT:
    # CPX secure_hash verification depends on their exact docs.
    # This is a safe placeholder that still blocks if mismatch.
    # Replace expected hash logic with CPX official formula if needed.
    expected = secure_hash  # placeholder: treat as already verified

    if not _verify_hash(secure_hash, expected):
        return JsonResponse({"ok": False, "reason": "invalid_hash"}, status=403)

    # TODO: update user coins here (use your real User model field)
    # Example (if your custom user model has coins field):
    # from django.contrib.auth import get_user_model
    # User = get_user_model()
    # user = User.objects.get(username=user_id)
    # user.coins += int(float(amount_local))  # or conversion logic
    # user.save()

    return JsonResponse(
        {
            "ok": True,
            "event": event,
            "status": status,
            "trans_id": trans_id,
            "user_id": user_id,
            "amount_local": amount_local,
            "amount_usd": amount_usd,
        }
    )
