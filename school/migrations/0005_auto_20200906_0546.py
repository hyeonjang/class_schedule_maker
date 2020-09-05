# Generated by Django 3.1.1 on 2020-09-05 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_auto_20200906_0403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='term',
            name='holiday',
        ),
        migrations.AddField(
            model_name='classroom',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.term'),
        ),
        migrations.AddField(
            model_name='subject',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.term'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='grade',
            field=models.PositiveSmallIntegerField(choices=[(4, '4학년'), (3, '3학년'), (6, '6학년'), (2, '2학년'), (1, '1학년'), (5, '5학년')], default=1),
        ),
        migrations.AlterField(
            model_name='subject',
            name='grade',
            field=models.PositiveSmallIntegerField(choices=[(4, '4학년'), (3, '3학년'), (6, '6학년'), (2, '2학년'), (1, '1학년'), (5, '5학년')]),
        ),
    ]
