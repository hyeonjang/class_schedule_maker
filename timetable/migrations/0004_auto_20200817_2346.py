# Generated by Django 3.1 on 2020-08-17 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_timetable_create_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='create_at',
            new_name='created_time',
        ),
    ]
