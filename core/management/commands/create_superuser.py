"""
Django management command to create a superuser non-interactively.
Run: python manage.py create_superuser
Or set environment variables: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser non-interactively'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Superuser username',
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Superuser email',
            default=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@nepearn.com')
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Superuser password',
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', None)
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Skip confirmation prompts',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        noinput = options['noinput']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Skipping creation.')
            )
            return

        # If no password provided, generate a random one
        if not password:
            import secrets
            password = secrets.token_urlsafe(16)
            self.stdout.write(
                self.style.WARNING(f'No password provided. Generated random password: {password}')
            )
            self.stdout.write(
                self.style.WARNING('Please save this password! It will not be shown again.')
            )

        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
            if not options.get('password'):
                self.stdout.write(
                    self.style.SUCCESS(f'Password: {password}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )

