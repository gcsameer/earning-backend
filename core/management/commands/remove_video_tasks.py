"""
Remove/deactivate all video tasks.
Run: python manage.py remove_video_tasks
"""
from django.core.management.base import BaseCommand
from core.models import Task


class Command(BaseCommand):
    help = 'Deactivates all video tasks'

    def handle(self, *args, **options):
        video_tasks = Task.objects.filter(type='video')
        count = video_tasks.count()
        
        if count > 0:
            video_tasks.update(is_active=False)
            self.stdout.write(
                self.style.SUCCESS(f'✅ Deactivated {count} video task(s)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No video tasks found to deactivate')
            )

