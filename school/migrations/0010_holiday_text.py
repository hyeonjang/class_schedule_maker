# Generated by Django 3.1.1 on 2020-09-26 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_auto_20200925_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='text',
            field=models.TextField(default='explanation'),
        ),
    ]