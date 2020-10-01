# Generated by Django 3.1.1 on 2020-10-01 15:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('text', models.TextField(default='explanation')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('semester', models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('grade', models.PositiveSmallIntegerField(choices=[(1, '1학년'), (2, '2학년'), (3, '3학년'), (4, '4학년'), (5, '5학년'), (6, '6학년')])),
                ('count', models.IntegerField(default=272, validators=[django.core.validators.MinValueValidator(64), django.core.validators.MaxValueValidator(448)])),
            ],
            options={
                'unique_together': {('name', 'grade')},
            },
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveSmallIntegerField(choices=[(1, '1학년'), (2, '2학년'), (3, '3학년'), (4, '4학년'), (5, '5학년'), (6, '6학년')], default=1)),
                ('number', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('student_count', models.PositiveSmallIntegerField(default=1, null=True)),
                ('teacher', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('grade', 'number')},
            },
        ),
    ]
