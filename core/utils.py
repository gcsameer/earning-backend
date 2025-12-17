from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

from .models import FraudEvent, UserTask

User = get_user_model()


# -------------------------------------
# FRAUD LOGGING
# -------------------------------------
def record_fraud_event(user, ip_address, device_id, event_type, score, reason):
    """
    Record a fraud event & update the user's fraud score.
    Does NOT block the user by itself.
    """
    # Update total fraud score
    user.fraud_score += score
    user.save(update_fields=["fraud_score"])

    # Store detailed event
    FraudEvent.objects.create(
        user=user,
        event_type=event_type,
        score=score,
        reason=reason,
        ip_address=ip_address,
        device_id=device_id,
    )


# -------------------------------------
# TASK SPEED CHECK
# -------------------------------------
def check_task_speed(user_task, min_seconds=8):
    """
    Ensure user spent realistic time on the task.
    If task completed too fast → log fraud + block earning.
    """

    if not user_task.completed_at:
        return  # should never happen

    duration = (user_task.completed_at - user_task.started_at).total_seconds()

    # If completed too fast = cheating
    if duration < min_seconds:
        record_fraud_event(
            user=user_task.user,
            ip_address=user_task.ip_address,
            device_id=user_task.device_id,
            event_type="suspicious_speed",
            score=5.0,
            reason=f"Task {user_task.task_id} completed in {duration}s (< {min_seconds}s).",
        )

        raise PermissionDenied(
            "Task completed too fast — possible fraud detected."
        )


# -------------------------------------
# DAILY TASK LIMIT CHECK
# -------------------------------------
def check_daily_task_limit(user, max_tasks_per_day=3):
    """
    Prevent user from exceeding daily task limit.
    Blocks new tasks when limit reached.
    Excludes offerwall and game-based tasks from the count.
    Game-based tasks (scratch_card, spin_wheel, puzzle, quiz) have their own per-type limits.
    """

    today = timezone.now().date()

    # Count only non-offerwall and non-game tasks started today
    # Exclude offerwall tasks and game-based tasks from daily limit
    # Game tasks have their own per-type limits (3 times per type)
    game_types = ["scratch_card", "spin_wheel", "puzzle", "quiz"]
    count_today = UserTask.objects.filter(
        user=user,
        started_at__date=today
    ).exclude(
        task__type__in=["offerwall", "tapjoy_offerwall"] + game_types  # Exclude offerwall and game tasks from daily limit
    ).count()

    if count_today >= max_tasks_per_day:

        # Log fraud activity
        record_fraud_event(
            user=user,
            ip_address=None,
            device_id=user.device_id,
            event_type="limit_exceeded",
            score=10.0,
            reason=f"User attempted more than {max_tasks_per_day} tasks today (count={count_today}).",
        )

        raise PermissionDenied(
            f"Daily task limit reached ({max_tasks_per_day} tasks per day). Try again tomorrow."
        )
