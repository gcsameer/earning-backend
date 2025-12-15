"""
Django management command to set up default settings.
Run: python manage.py setup_settings
"""
from django.core.management.base import BaseCommand
from core.models import Settings


class Command(BaseCommand):
    help = 'Sets up default settings (COIN_TO_RS_RATE, etc.)'

    def handle(self, *args, **options):
        # Default settings
        settings_data = [
            {
                'key': 'COIN_TO_RS_RATE',
                'value': '0.1',  # 1 coin = Rs 0.1
                'description': 'Conversion rate: 1 coin = Rs 0.1'
            },
            {
                'key': 'MIN_WITHDRAW_RS',
                'value': '50',  # Minimum Rs 50 to withdraw
                'description': 'Minimum withdrawal amount in Rs'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for setting_data in settings_data:
            setting, created = Settings.objects.get_or_create(
                key=setting_data['key'],
                defaults={'value': setting_data['value']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created setting: {setting_data["key"]} = {setting_data["value"]}')
                )
            else:
                # Update existing setting
                setting.value = setting_data['value']
                setting.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Updated setting: {setting_data["key"]} = {setting_data["value"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Setup complete! Created {created_count} settings, updated {updated_count} settings.')
        )
        
        # Display current settings
        self.stdout.write('\n📋 Current Settings:')
        for setting in Settings.objects.all():
            self.stdout.write(f'  {setting.key} = {setting.value}')

