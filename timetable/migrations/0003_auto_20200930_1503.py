# Generated by Django 3.1.1 on 2020-09-30 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_remove_invited_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hometable',
            name='is_subject_time',
        ),
        migrations.RemoveField(
            model_name='invited',
            name='is_subject_time',
        ),
        migrations.RemoveField(
            model_name='subjecttable',
            name='is_subject_time',
        ),
    ]
