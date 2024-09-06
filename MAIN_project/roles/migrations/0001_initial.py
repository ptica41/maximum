# Generated by Django 4.2.7 on 2024-04-03 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schooldb', verbose_name='Школа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Родители',
                'db_table': 'Parents',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_school', to='main_app.schooldb', verbose_name='Школа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Тьюторы',
                'db_table': 'Tutors',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schooldb', verbose_name='Школа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Учителя',
                'db_table': 'Teachers',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schooldb', verbose_name='Школа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Ученики',
                'db_table': 'Students',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ParentChild',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='roles.student', verbose_name='Ребенок')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='roles.parent', verbose_name='Родитель')),
            ],
            options={
                'verbose_name_plural': 'Родители и дети',
                'db_table': 'ParentChild',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schooldb', verbose_name='Школа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Операторы питания',
                'db_table': 'Foods',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FacultativeTeacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schooldb', verbose_name='Школа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Учителя факультативов',
                'db_table': 'FacultativeTeachers',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schooldb', verbose_name='Школа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Завучи',
                'db_table': 'Directors',
                'ordering': ['-id'],
            },
        ),
    ]