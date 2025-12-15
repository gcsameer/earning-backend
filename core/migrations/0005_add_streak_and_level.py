# Generated migration for login streak and user level
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longest_streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='user_level',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='total_experience',
            field=models.IntegerField(default=0),
        ),
    ]

