# Generated by Django 4.2.7 on 2024-04-03 10:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to='', verbose_name='Фотография')),
                ('photo_min', models.ImageField(blank=True, null=True, upload_to='min', verbose_name='Превью')),
            ],
            options={
                'verbose_name_plural': 'Фотографии',
                'db_table': 'Photos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SchoolDB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название школы')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активная школа?')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='school_photo', to='main_app.photo', verbose_name='Фотография')),
            ],
            options={
                'verbose_name_plural': 'Школы',
                'db_table': 'SchoolsDB',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Юзернейм')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество')),
                ('male', models.CharField(blank=True, choices=[('MALE', 'male'), ('FEMALE', 'female')], null=True, verbose_name='Пол')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Эл. почта')),
                ('passport_series', models.CharField(blank=True, max_length=50, null=True, verbose_name='Серия паспорта')),
                ('passport_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер паспорта')),
                ('certificate_series', models.CharField(blank=True, max_length=50, null=True, verbose_name='Серия свидетельства о рождении')),
                ('certificate_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер свидетельства о рождении')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный пользователь?')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Онлайн')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Админ?')),
                ('role_is_active', models.BooleanField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_photo', to='main_app.photo', verbose_name='Фотография')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Пользователи',
                'db_table': 'Users',
                'ordering': ['-id'],
            },
        ),
    ]