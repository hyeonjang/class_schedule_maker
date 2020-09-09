# Generated by Django 3.1.1 on 2020-09-09 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0002_auto_20200909_1516'),
        ('timetable', '0003_invitedtable'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InvitedTable',
            new_name='Invited',
        ),
        migrations.AddField(
            model_name='hometable',
            name='inv_teacher',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetable.invited'),
        ),
    ]
