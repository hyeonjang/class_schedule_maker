# Generated by Django 3.1.1 on 2020-09-25 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200925_1552'),
        ('school', '0006_auto_20200916_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='teacher',
            field=models.OneToOneField(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_name', to='accounts.hometeacher'),
        ),
    ]
