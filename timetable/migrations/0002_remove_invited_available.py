# Generated by Django 3.1.1 on 2020-09-28 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invited',
            name='available',
        ),
    ]
