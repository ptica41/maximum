# Generated by Django 4.2.7 on 2024-04-03 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_schedule_date_schedule_end_schedule_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='date',
        ),
    ]
