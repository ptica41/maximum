# Generated by Django 4.2.7 on 2024-04-03 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_remove_schedule_date_remove_schedule_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='date',
            field=models.DateTimeField(default='2000-01-01T00:00:00+00:00', verbose_name='Дата'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Измененное завершение урока'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='number',
            field=models.IntegerField(choices=[(1, 'Урок 1'), (2, 'Урок 2'), (3, 'Урок 3'), (4, 'Урок 4'), (5, 'Урок 5'), (6, 'Урок 6'), (7, 'Урок 7'), (8, 'Урок 8'), (9, 'Урок 9'), (10, 'Урок 10')], default=1, verbose_name='Номер урока'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Измененное начало урока'),
        ),
    ]
