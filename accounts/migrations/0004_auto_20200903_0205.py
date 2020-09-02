# Generated by Django 3.1 on 2020-09-02 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20200903_0205'),
        ('accounts', '0003_auto_20200903_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=53),
        ),
        migrations.AlterField(
            model_name='user',
            name='classRoom',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.classroom'),
        ),
    ]
