# Generated by Django 4.2.7 on 2024-04-03 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0004_remove_schedule_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='date',
            field=models.DateTimeField(default='2000-01-01T00:00:00+00:00', verbose_name='Дата'),
        ),
    ]
