from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Partner1C(models.Model):

    objects = models.Manager()

    CHOICES = [
        ('MALE', 'male'),
        ('FEMALE', 'female'),
    ]

    UID = models.CharField(verbose_name='UID', max_length=128)
    surname = models.CharField(verbose_name='Фамилия', max_length=50)
    name = models.CharField(verbose_name='Имя', max_length=50, blank=True, null=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True, null=True)
    male = models.CharField(verbose_name='Пол', choices=CHOICES, blank=True, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    phone = PhoneNumberField(verbose_name='Телефон', blank=True, null=True)
    passport_series = models.CharField(verbose_name='Серия паспорта', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С
    passport_number = models.CharField(verbose_name='Номер паспорта', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С

    class Meta:
        db_table = "Partners1C"
        verbose_name_plural = "Сотрудники 1C"
        ordering = ["-id"]

    def __str__(self):
        return f'{self.surname} {self.name}'


class ParentChild1C(models.Model):

    objects = models.Manager()

    CHOICES = [
        ('MALE', 'male'),
        ('FEMALE', 'female'),
    ]

    child_UID = models.CharField(verbose_name='UID ребенка', max_length=128)
    child_surname = models.CharField(verbose_name='Фамилия ребенка', max_length=50)
    child_name = models.CharField(verbose_name='Имя ребенка', max_length=50, blank=True, null=True)
    child_middle_name = models.CharField(verbose_name='Отчество ребенка', max_length=255, blank=True, null=True)
    child_male = models.CharField(verbose_name='Пол ребенка', choices=CHOICES, blank=True, null=True)
    child_birthday = models.DateField(verbose_name='Дата рождения ребенка', blank=True, null=True)
    child_passport_series = models.CharField(verbose_name='Серия паспорта ребенка', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С
    child_passport_number = models.CharField(verbose_name='Номер паспорта ребенка', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С
    child_certificate_series = models.CharField(verbose_name='Серия свидетельства о рождении ребенка', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С
    child_certificate_number = models.CharField(verbose_name='Номер свидетельства о рождении ребенка', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С
    parent_UID = models.CharField(verbose_name='UID родителя', max_length=128)
    parent_surname = models.CharField(verbose_name='Фамилия родителя', max_length=50)
    parent_name = models.CharField(verbose_name='Имя родителя', max_length=50, blank=True, null=True)
    parent_middle_name = models.CharField(verbose_name='Отчество родителя', max_length=255, blank=True, null=True)
    parent_male = models.CharField(verbose_name='Пол родителя', choices=CHOICES, blank=True, null=True)
    parent_birthday = models.DateField(verbose_name='Дата рождения родителя', blank=True, null=True)
    parent_passport_series = models.CharField(verbose_name='Серия паспорта родителя', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С
    parent_passport_number = models.CharField(verbose_name='Номер паспорта родителя', max_length=50, blank=True, null=True)  # INTEGER не подходит из-за вне диапазона значений и кривизны данных из 1С
    parent_phone = PhoneNumberField(verbose_name='Телефон родителя', blank=True, null=True)

    class Meta:
        db_table = "ParentChild1C"
        verbose_name_plural = "Родители-дети 1C"
        ordering = ["-id"]

    def __str__(self):
        return f'Ребенок: {self.child_surname} {self.child_name} | Родитель: {self.parent_surname} {self.parent_name}'
