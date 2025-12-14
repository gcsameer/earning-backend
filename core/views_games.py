"""
Game-based task views (scratch card, spin wheel, puzzle, quiz)
These tasks are completed instantly and reward coins automatically.
"""
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
import random

from .models import Task, UserTask, WalletTransaction
from .serializers import TaskSerializer
from .utils import check_daily_task_limit
from .views import get_client_ip


class GameTaskCompleteView(APIView):
    """
    Complete game-based tasks instantly (scratch card, spin wheel, puzzle, quiz).
    These tasks don't require a countdown - coins are awarded immediately.
    """
    
    def post(self, request, task_id):
        try:
            user = request.user
            
            # DAILY LIMIT CHECK
            try:
                check_daily_task_limit(user)
            except PermissionDenied as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # DAILY EARNING LIMIT
            if not user.can_earn_now(max_per_day=100):
                return Response(
                    {"detail": "Daily earning limit reached. Try again tomorrow."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get task
            try:
                task = Task.objects.get(id=task_id, is_active=True)
            except Task.DoesNotExist:
                return Response(
                    {"detail": "Task not found or inactive"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Only allow game-based tasks
            allowed_types = ["scratch_card", "spin_wheel", "puzzle", "quiz"]
            if task.type not in allowed_types:
                return Response(
                    {"detail": "This endpoint is only for game-based tasks"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user already completed this task today
            today = timezone.now().date()
            existing_task = UserTask.objects.filter(
                user=user,
                task=task,
                status="completed",
                completed_at__date=today
            ).first()
            
            if existing_task:
                return Response(
                    {"detail": "You have already completed this task today"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate reward based on task type
            if task.type == "scratch_card":
                # Scratch Card: 20-150 coins (random)
                reward = random.randint(20, 150)
            elif task.type == "spin_wheel":
                # Spin Wheel: 20-150 coins (random)
                reward = random.randint(20, 150)
            elif task.type == "puzzle":
                # Math Puzzle: 50 coins (fixed)
                reward = 50
            elif task.type == "quiz":
                # Quick Quiz: 50 coins (fixed)
                reward = 50
            else:
                # Default: use task.reward_coins if set, otherwise 0
                reward = task.reward_coins if task.reward_coins and task.reward_coins > 0 else 0
            
            if reward <= 0:
                return Response(
                    {"detail": "Invalid reward amount"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ip = get_client_ip(request)
            device_id = request.data.get("device_id", "")
            
            # Create and mark as completed immediately
            user_task = UserTask.objects.create(
                user=user,
                task=task,
                status="completed",
                started_at=timezone.now(),
                completed_at=timezone.now(),
                ip_address=ip,
                device_id=device_id,
            )
            
            # Award coins immediately (with transaction safety)
            user.register_earn()
            user.coins_balance += reward
            user.save(update_fields=["coins_balance", "last_earn_date", "daily_earn_count", "last_earn_time"])
            
            # Create wallet transaction
            WalletTransaction.objects.create(
                user=user,
                type="earn",
                coins=reward,
                note=f"Completed {task.get_type_display()}: {task.title}",
            )
            
            return Response({
                "message": "Task completed successfully",
                "reward_coins": reward,
                "new_balance": user.coins_balance,
                "task": TaskSerializer(task).data,
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error completing game task: {str(e)}", exc_info=True)
            
            return Response(
                {"detail": f"Failed to complete task: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

