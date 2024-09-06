# Generated by Django 4.2.7 on 2024-04-03 10:52

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParentChild1C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_UID', models.CharField(max_length=128, verbose_name='UID ребенка')),
                ('child_surname', models.CharField(max_length=50, verbose_name='Фамилия ребенка')),
                ('child_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя ребенка')),
                ('child_middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество ребенка')),
                ('child_male', models.CharField(blank=True, choices=[('MALE', 'male'), ('FEMALE', 'female')], null=True, verbose_name='Пол ребенка')),
                ('child_birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения ребенка')),
                ('child_passport_series', models.CharField(blank=True, max_length=50, null=True, verbose_name='Серия паспорта ребенка')),
                ('child_passport_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер паспорта ребенка')),
                ('child_certificate_series', models.CharField(blank=True, max_length=50, null=True, verbose_name='Серия свидетельства о рождении ребенка')),
                ('child_certificate_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер свидетельства о рождении ребенка')),
                ('parent_UID', models.CharField(max_length=128, verbose_name='UID родителя')),
                ('parent_surname', models.CharField(max_length=50, verbose_name='Фамилия родителя')),
                ('parent_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя родителя')),
                ('parent_middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество родителя')),
                ('parent_male', models.CharField(blank=True, choices=[('MALE', 'male'), ('FEMALE', 'female')], null=True, verbose_name='Пол родителя')),
                ('parent_birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения родителя')),
                ('parent_passport_series', models.CharField(blank=True, max_length=50, null=True, verbose_name='Серия паспорта родителя')),
                ('parent_passport_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер паспорта родителя')),
                ('parent_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон родителя')),
            ],
            options={
                'verbose_name_plural': 'Родители-дети 1C',
                'db_table': 'ParentChild1C',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Partner1C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.CharField(max_length=128, verbose_name='UID')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество')),
                ('male', models.CharField(blank=True, choices=[('MALE', 'male'), ('FEMALE', 'female')], null=True, verbose_name='Пол')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                ('passport_series', models.CharField(blank=True, max_length=50, null=True, verbose_name='Серия паспорта')),
                ('passport_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер паспорта')),
            ],
            options={
                'verbose_name_plural': 'Сотрудники 1C',
                'db_table': 'Partners1C',
                'ordering': ['-id'],
            },
        ),
    ]