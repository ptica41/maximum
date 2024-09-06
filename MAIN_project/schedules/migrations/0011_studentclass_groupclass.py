# Generated by Django 4.2.7 on 2024-04-18 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
        ('schedules', '0010_alter_timelesson_lesson10_end_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cls_student', to='schedules.class', verbose_name='Класс')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_cls', to='roles.student', verbose_name='Ученик')),
            ],
            options={
                'verbose_name_plural': 'Ученики и классы',
                'db_table': 'StudentClasses',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GroupClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_student', to='schedules.group', verbose_name='Класс')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_group', to='roles.student', verbose_name='Ученик')),
            ],
            options={
                'verbose_name_plural': 'Ученики и группы',
                'db_table': 'StudentGroups',
                'ordering': ['-id'],
            },
        ),
    ]