# Generated by Django 3.1 on 2020-09-02 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200903_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='user',
            name='is_homeroom',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_subject',
            field=models.BooleanField(default=True),
        ),
    ]
