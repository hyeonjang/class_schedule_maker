# Generated by Django 3.1.1 on 2020-09-07 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200907_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='assigned_subjects_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='classRoom',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subject1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subject2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subject3',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subject4',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subject5',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subject6',
        ),
    ]
