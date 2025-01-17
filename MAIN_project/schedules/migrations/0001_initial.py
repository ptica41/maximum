# Generated by Django 4.2.7 on 2024-04-03 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('roles', '0001_initial'),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cabinet_school', to='main_app.schooldb', verbose_name='Школа')),
            ],
            options={
                'verbose_name_plural': 'Кабинеты',
                'db_table': 'Cabinets',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('cabinet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_cabinet', to='schedules.cabinet', verbose_name='Кабинет')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_tutor', to='roles.tutor', verbose_name='Тьютор')),
            ],
            options={
                'verbose_name_plural': 'Классы',
                'db_table': 'Classes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('cls', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_class', to='schedules.class', verbose_name='Класс')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_school', to='main_app.schooldb', verbose_name='Школа')),
            ],
            options={
                'verbose_name_plural': 'Группы',
                'db_table': 'Groups',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('facultative_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facultative_teacher', to='roles.facultativeteacher', verbose_name='Учитель факультатива')),
            ],
            options={
                'verbose_name_plural': 'Уроки',
                'db_table': 'Lessons',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TimeLesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('period', models.CharField(max_length=255, verbose_name='Период действия')),
                ('lesson1_start', models.DateTimeField(verbose_name='Начало урока 1')),
                ('lesson1_end', models.DateTimeField(verbose_name='Конец урока 1')),
                ('lesson2_start', models.DateTimeField(verbose_name='Начало урока 2')),
                ('lesson2_end', models.DateTimeField(verbose_name='Конец урока 2')),
                ('lesson3_start', models.DateTimeField(verbose_name='Начало урока 3')),
                ('lesson3_end', models.DateTimeField(verbose_name='Конец урока 3')),
                ('lesson4_start', models.DateTimeField(verbose_name='Начало урока 4')),
                ('lesson4_end', models.DateTimeField(verbose_name='Конец урока 4')),
                ('lesson5_start', models.DateTimeField(verbose_name='Начало урока 5')),
                ('lesson5_end', models.DateTimeField(verbose_name='Конец урока 5')),
                ('lesson6_start', models.DateTimeField(verbose_name='Начало урока 6')),
                ('lesson6_end', models.DateTimeField(verbose_name='Конец урока 6')),
                ('lesson7_start', models.DateTimeField(blank=True, null=True, verbose_name='Начало урока 7')),
                ('lesson7_end', models.DateTimeField(blank=True, null=True, verbose_name='Конец урока 7')),
                ('lesson8_start', models.DateTimeField(blank=True, null=True, verbose_name='Начало урока 8')),
                ('lesson8_end', models.DateTimeField(blank=True, null=True, verbose_name='Конец урока 8')),
                ('lesson9_start', models.DateTimeField(blank=True, null=True, verbose_name='Начало урока 9')),
                ('lesson9_end', models.DateTimeField(blank=True, null=True, verbose_name='Конец урока 9')),
                ('lesson10_start', models.DateTimeField(blank=True, null=True, verbose_name='Начало урока 10')),
                ('lesson10_end', models.DateTimeField(blank=True, null=True, verbose_name='Конец урока 10')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time_lesson_school', to='main_app.schooldb', verbose_name='Школа')),
            ],
            options={
                'verbose_name_plural': 'Время уроков',
                'db_table': 'TimeLessons',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(verbose_name='Дата')),
                ('number', models.IntegerField(choices=[(1, 'Урок 1'), (2, 'Урок 2'), (3, 'Урок 3'), (4, 'Урок 4'), (5, 'Урок 5'), (6, 'Урок 6'), (7, 'Урок 7'), (8, 'Урок 8'), (9, 'Урок 9'), (10, 'Урок 10')], verbose_name='Номер урока')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='Измененное начало урока')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='Измененное завершение урока')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий к уроку')),
                ('replace_comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий к замене урока')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='Отмена урока')),
                ('cancelled_comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий к отмене урока')),
                ('cabinet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_cabinet', to='schedules.cabinet', verbose_name='Кабинет')),
                ('cls', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_class', to='schedules.class', verbose_name='Класс')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_group', to='schedules.group', verbose_name='Группа')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson', to='schedules.lesson', verbose_name='Урок')),
                ('lesson_replace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson_replace', to='schedules.lesson', verbose_name='Замена урока')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_student', to='roles.student', verbose_name='Ученик')),
                ('time_lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_time', to='schedules.timelesson', verbose_name='Время уроков')),
            ],
            options={
                'verbose_name_plural': 'Уроки для расписания',
                'db_table': 'Schedules',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='object_school', to='main_app.schooldb', verbose_name='Школа')),
            ],
            options={
                'verbose_name_plural': 'Предметы',
                'db_table': 'Objects',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson_object', to='schedules.object', verbose_name='Предмет'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher', to='roles.teacher', verbose_name='Учитель'),
        ),
    ]
