"""
Django management command to create sample game tasks.
Run: python manage.py create_game_tasks
"""
from django.core.management.base import BaseCommand
from core.models import Task


class Command(BaseCommand):
    help = 'Creates sample game tasks (scratch card, spin wheel, puzzle, quiz)'

    def handle(self, *args, **options):
        tasks_data = [
            {
                'type': 'scratch_card',
                'title': 'Scratch Card - Win Coins!',
                'description': 'Scratch the card to reveal your reward. Win between 5-20 coins!',
                'reward_coins': 0,  # Will be random 5-20
                'is_active': True,
            },
            {
                'type': 'spin_wheel',
                'title': 'Spin the Wheel',
                'description': 'Spin the wheel and win coins! Each spin can reward 5-20 coins.',
                'reward_coins': 0,  # Will be random 5-20
                'is_active': True,
            },
            {
                'type': 'puzzle',
                'title': 'Math Puzzle',
                'description': 'Solve a simple math puzzle to earn coins. Win 5-20 coins for correct answers!',
                'reward_coins': 0,  # Will be random 5-20
                'is_active': True,
            },
            {
                'type': 'quiz',
                'title': 'Quick Quiz',
                'description': 'Answer a quiz question correctly to win coins! Earn 5-20 coins per correct answer.',
                'reward_coins': 0,  # Will be random 5-20
                'is_active': True,
            },
        ]

        created_count = 0
        for task_data in tasks_data:
            task, created = Task.objects.get_or_create(
                type=task_data['type'],
                title=task_data['title'],
                defaults=task_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created task: {task.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Task already exists: {task.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nCreated {created_count} new game tasks!')
        )

