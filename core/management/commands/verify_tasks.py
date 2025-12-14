"""
Django management command to verify tasks exist in the database.
Run: python manage.py verify_tasks
"""
from django.core.management.base import BaseCommand
from core.models import Task


class Command(BaseCommand):
    help = 'Verifies that tasks exist in the database'

    def handle(self, *args, **options):
        all_tasks = Task.objects.all()
        active_tasks = Task.objects.filter(is_active=True)
        
        self.stdout.write(self.style.SUCCESS(f'\n📊 Task Statistics:'))
        self.stdout.write(f'   Total tasks: {all_tasks.count()}')
        self.stdout.write(f'   Active tasks: {active_tasks.count()}')
        
        if active_tasks.count() == 0:
            self.stdout.write(self.style.ERROR('\n❌ No active tasks found!'))
            self.stdout.write(self.style.WARNING('   Run: python manage.py create_game_tasks'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ Active Tasks:'))
            for task in active_tasks:
                self.stdout.write(f'   - {task.title} ({task.type}) - {task.reward_coins} coins')
        
        self.stdout.write('')

