# Generated by Django 3.1.1 on 2020-10-07 18:48

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
            name='SubjectTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('time', models.SmallIntegerField(blank=True, default=0)),
                ('is_event_or_holi', models.BooleanField(default=False)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.classroom')),
                ('semester', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='school.term')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_sub_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'unique_together': {('day', 'time', 'teacher')},
            },
        ),
        migrations.CreateModel(
            name='Invited',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('time', models.SmallIntegerField(blank=True, default=0)),
                ('is_event_or_holi', models.BooleanField(default=False)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.classroom')),
                ('semester', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='school.term')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invited_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'unique_together': {('day', 'time', 'teacher')},
            },
        ),
        migrations.CreateModel(
            name='HomeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('time', models.SmallIntegerField(blank=True, default=0)),
                ('is_event_or_holi', models.BooleanField(default=False)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.classroom')),
                ('inv_teacher', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetable.invited')),
                ('semester', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='school.term')),
                ('sub_teacher', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetable.subjecttable')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_home_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'unique_together': {('day', 'time', 'teacher')},
            },
        ),
    ]
