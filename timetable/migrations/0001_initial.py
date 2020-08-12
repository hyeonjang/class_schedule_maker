# Generated by Django 3.1 on 2020-08-12 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classGrade', models.SmallIntegerField(default=0)),
                ('classNumber', models.SmallIntegerField(default=0)),
                ('weekDay', models.CharField(max_length=50)),
                ('time', models.CharField(max_length=50)),
                ('semester', models.IntegerField(default=0)),
                ('subject', models.CharField(max_length=50)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='sTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable')),
            ],
        ),
        migrations.CreateModel(
            name='sTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable')),
            ],
        ),
        migrations.CreateModel(
            name='sSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable')),
            ],
        ),
        migrations.CreateModel(
            name='sClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable')),
            ],
        ),
    ]
