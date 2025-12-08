from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import FraudEvent, UserTask

User = get_user_model()


def record_fraud_event(user, ip_address, device_id, event_type, score, reason):
    user.fraud_score += score
    user.save()

    FraudEvent.objects.create(
        user=user,
        event_type=event_type,
        score=score,
        reason=reason,
        ip_address=ip_address,
        device_id=device_id,
    )


def check_task_speed(user_task, min_seconds: int = 5):
    if not user_task.completed_at:
        return

    delta = (user_task.completed_at - user_task.started_at).total_seconds()
    if delta < min_seconds:
        record_fraud_event(
            user=user_task.user,
            ip_address=user_task.ip_address,
            device_id=user_task.device_id,
            event_type="suspicious_speed",
            score=5.0,
            reason=f"Task {user_task.task_id} completed in {delta} seconds (< {min_seconds}).",
        )


def check_daily_task_limit(user, max_tasks_per_day: int = 50):
    today = timezone.now().date()
    count_today = UserTask.objects.filter(
        user=user,
        started_at__date=today,
    ).count()
    if count_today > max_tasks_per_day:
        record_fraud_event(
            user=user,
            ip_address=None,
            device_id=user.device_id,
            event_type="limit_exceeded",
            score=10.0,
            reason=f"Completed {count_today} tasks today (limit {max_tasks_per_day}).",
        )

def check_task_speed(user_task):
    min_seconds = 8

    if not user_task.completed_at:
        return

    duration = (user_task.completed_at - user_task.started_at).total_seconds()

    if duration < min_seconds:
        from .models import FraudEvent

        FraudEvent.objects.create(
            user=user_task.user,
            event_type="suspicious_speed",
            score=5,
            reason=f"Completed in {duration}s which is less than minimum {min_seconds}s",
            ip_address=user_task.ip_address,
            device_id=user_task.device_id
        )
        raise Exception("Task completed too fast. Fraud detected.")
