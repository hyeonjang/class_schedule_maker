# Generated by Django 3.1 on 2020-09-03 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('time', models.SmallIntegerField(blank=True, default=0)),
                ('created_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('classRoom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.classroom')),
                ('semester', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='school.term')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('weekday', 'time')},
            },
        ),
    ]
