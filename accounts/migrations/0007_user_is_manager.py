# Generated by Django 3.1 on 2020-09-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200903_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_manager',
            field=models.BooleanField(default=True),
        ),
    ]
