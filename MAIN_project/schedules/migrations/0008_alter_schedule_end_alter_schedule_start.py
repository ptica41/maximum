# Generated by Django 4.2.7 on 2024-04-11 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0007_remove_schedule_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(verbose_name='Измененное завершение урока'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(verbose_name='Измененное начало урока'),
        ),
    ]
