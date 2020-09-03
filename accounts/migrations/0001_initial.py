# Generated by Django 3.1 on 2020-09-03 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('name', models.CharField(default='', max_length=53)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_subject', models.BooleanField(default=False)),
                ('is_homeroom', models.BooleanField(default=True)),
                ('assigned_subjects_number', models.SmallIntegerField(blank=True, default=1, null=True)),
                ('classRoom', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.classroom')),
                ('subject1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='one', to='school.subject')),
                ('subject2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='two', to='school.subject')),
                ('subject3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='three', to='school.subject')),
                ('subject4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='four', to='school.subject')),
                ('subject5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='five', to='school.subject')),
                ('subject6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='six', to='school.subject')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
