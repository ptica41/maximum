# Generated by Django 4.2.7 on 2024-04-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0008_alter_schedule_end_alter_schedule_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='number',
            field=models.IntegerField(blank=True, choices=[(1, 'Урок 1'), (2, 'Урок 2'), (3, 'Урок 3'), (4, 'Урок 4'), (5, 'Урок 5'), (6, 'Урок 6'), (7, 'Урок 7'), (8, 'Урок 8'), (9, 'Урок 9'), (10, 'Урок 10')], null=True, verbose_name='Номер урока'),
        ),
    ]
