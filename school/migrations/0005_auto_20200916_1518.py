# Generated by Django 3.1.1 on 2020-09-16 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_invitedteacher'),
        ('school', '0004_auto_20200916_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='tea',
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='to_teacher', to='accounts.hometeacher'),
        ),
    ]
