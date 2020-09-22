# Generated by Django 3.1.1 on 2020-09-16 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0002_auto_20200909_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='student_count',
            field=models.PositiveSmallIntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]