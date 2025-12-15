"""
Django management command to update superuser password.
Run: python manage.py update_superuser_password --username admin --password newpassword
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Updates a superuser password'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Superuser username',
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        )
        parser.add_argument(
            '--password',
            type=str,
            help='New password',
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', None),
            required=True
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Password updated for user "{username}" successfully!')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating password: {str(e)}')
            )

