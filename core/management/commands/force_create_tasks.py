"""
Force create all game tasks, deleting existing ones first.
Run: python manage.py force_create_tasks
"""
from django.core.management.base import BaseCommand
from core.models import Task


class Command(BaseCommand):
    help = 'Force creates all game tasks by deleting existing ones first'

    def handle(self, *args, **options):
        tasks_data = [
            {
                'type': 'scratch_card',
                'title': 'Scratch Card - Win Coins!',
                'description': '🎫 Scratch the card to reveal your reward. Win between 20-150 coins instantly!',
                'reward_coins': 0,  # Will be random 20-150
                'is_active': True,
            },
            {
                'type': 'spin_wheel',
                'title': 'Spin the Wheel',
                'description': '🎡 Spin the wheel and win coins! Each spin can reward 20-150 coins instantly!',
                'reward_coins': 0,  # Will be random 20-150
                'is_active': True,
            },
            {
                'type': 'puzzle',
                'title': 'Math Puzzle',
                'description': 'Solve a simple math puzzle to earn coins. Win 50 coins for correct answers!',
                'reward_coins': 0,  # Will be 50 coins fixed
                'is_active': True,
            },
            {
                'type': 'quiz',
                'title': 'Quick Quiz',
                'description': 'Answer a quiz question correctly to win coins! Earn 50 coins per correct answer.',
                'reward_coins': 0,  # Will be 50 coins fixed
                'is_active': True,
            },
        ]

        # Delete existing game tasks and deactivate video tasks
        deleted_count = Task.objects.filter(
            type__in=['scratch_card', 'spin_wheel', 'puzzle', 'quiz']
        ).delete()[0]
        
        # Deactivate video tasks
        video_deactivated = Task.objects.filter(type='video', is_active=True).update(is_active=False)
        if video_deactivated > 0:
            self.stdout.write(
                self.style.WARNING(f'Deactivated {video_deactivated} video task(s)')
            )
        
        self.stdout.write(
            self.style.WARNING(f'Deleted {deleted_count} existing game tasks')
        )

        # Create new tasks
        created_tasks = []
        for task_data in tasks_data:
            task = Task.objects.create(**task_data)
            created_tasks.append(task)
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created: {task.title} (type: {task.type})')
            )

        # Verify
        all_active = Task.objects.filter(is_active=True)
        game_tasks = all_active.filter(type__in=['scratch_card', 'spin_wheel', 'puzzle', 'quiz'])
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Created {len(created_tasks)} game tasks!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Total active tasks: {all_active.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Game tasks: {game_tasks.count()}')
        )
        
        self.stdout.write('\n📋 Game Tasks:')
        for task in game_tasks:
            self.stdout.write(f'   - {task.title} ({task.type}) - Active: {task.is_active}')

