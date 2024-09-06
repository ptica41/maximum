import os

from io import BytesIO

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# from roles.models import Director, Teacher, FacultativeTeacher, Tutor, Parent, Student, Food, ParentChild


class UserManager(BaseUserManager):
    """
    Переопределяем менеджер пользователя под свои обязательные поля
    """

    def create_user(self, username, name, surname, password=None, commit=True, **kwargs):
        """
        Creates and saves a User with the given phone, name, surname and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not name:
            raise ValueError('Users must have a first name')
        if not surname:
            raise ValueError('Users must have a surname')

        user = self.model(username=username, name=name, surname=surname, **kwargs)

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, username, name, surname, password):
        """
        Creates and saves a superuser with the given phone, name, surname and password.
        """
        user = self.create_user(username, name, surname, password, commit=False)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Photo(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    photo = models.ImageField(verbose_name='Фотография', upload_to='')
    photo_min = models.ImageField(verbose_name="Превью", blank=True, null=True, upload_to='min')

    class Meta:
        db_table = "Photos"
        verbose_name_plural = "Фотографии"
        ordering = ["-id"]

    def __str__(self):  # указываем id в качестве "названия" при отображении экземпляров модели
        return f"(photoID {str(self.id)})"


@receiver(post_save, sender=Photo)
def create_min(sender, instance, created, **kwargs):
    """
    Устанавливаем обработчик события - при создании экземпляра модели Photo будет создаваться миниатюра и записываться в атрибут photo_min
    """
    if created:
        photo = instance.photo
        photo_name = photo.name

        photo_min = Image.open(photo)
        if photo_min.size[0] > 250:  # проверка ширины фотографии (более 250 пикселей)
            photo_min.thumbnail((250, photo_min.size[1]))
        buffer = BytesIO()
        photo_min.save(fp=buffer, format='PNG')  # записываем миниатюру в буфер
        pillow_image = ContentFile(buffer.getvalue())
        instance.photo_min.save(photo_name,
                                InMemoryUploadedFile(pillow_image, None, photo_name, 'image_jpeg', pillow_image.tell,
                                                     None))


@receiver(post_delete, sender=Photo)
def delete_from_storage(sender, instance, **kwargs):
    """
    Удаляем файлы фотографии и миниатюры из хранилища при удалении экземпляра модели Photo
    """
    if instance.photo and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)
    if instance.photo_min and os.path.isfile(instance.photo_min.path):
        os.remove(instance.photo_min.path)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    CHOICES = [
        ('MALE', 'male'),
        ('FEMALE', 'female'),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='Юзернейм', max_length=50, unique=True)
    surname = models.CharField(verbose_name='Фамилия', max_length=50)
    name = models.CharField(verbose_name='Имя', max_length=50)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True, null=True)
    male = models.CharField(verbose_name='Пол', choices=CHOICES, blank=True, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    phone = PhoneNumberField(verbose_name='Телефон', blank=True, null=True)
    email = models.EmailField(verbose_name='Эл. почта', blank=True, null=True)
    passport_series = models.CharField(verbose_name='Серия паспорта', max_length=50, blank=True, null=True)
    passport_number = models.CharField(verbose_name='Номер паспорта', max_length=50, blank=True, null=True)
    certificate_series = models.CharField(verbose_name='Серия свидетельства о рождении', max_length=50, blank=True,
                                          null=True)
    certificate_number = models.CharField(verbose_name='Номер свидетельства о рождении', max_length=50, blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный пользователь?', default=True)
    date_joined = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='Онлайн', blank=True, null=True)
    is_superuser = models.BooleanField(verbose_name='Админ?', default=False)
    photo = models.ForeignKey(Photo, verbose_name='Фотография', related_name='user_photo', on_delete=models.SET_NULL,
                              blank=True, null=True)
    role_is_active = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        db_table = "Users"
        verbose_name_plural = "Пользователи"
        ordering = ["-id"]

    def __str__(self):  # указываем фамилию и имя в качестве "названия" при отображении экземпляров модели
        return f"(userID {self.id}) {self.surname} {self.name}"

    @property
    def is_staff(self):  # Для админки бэкенда обязательно нужно поле is_staff - присваиваем значение is_superuser
        return self.is_superuser


class SchoolDB(models.Model):
    objects = models.Manager()

    CHOICES = [
        ('+00:00', 'UTC'),
        ('+01:00', 'UTC+1'),
        ('+02:00', 'UTC+2'),
        ('+03:00', 'UTC+3'),
        ('+04:00', 'UTC+4'),
        ('+05:00', 'UTC+5'),
        ('+06:00', 'UTC+6'),
        ('+07:00', 'UTC+7'),
        ('+08:00', 'UTC+8'),
        ('+09:00', 'UTC+9'),
        ('+10:00', 'UTC+10'),
        ('+11:00', 'UTC+11'),
        ('+12:00', 'UTC+12')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название школы', max_length=255, unique=True)
    # db_engine = models.CharField(verbose_name='СУБД', max_length=2, choices=CHOICES)
    # db_name = models.CharField(verbose_name='Название БД', max_length=50)
    # db_user = models.CharField(verbose_name='Имя пользователя БД', max_length=50)
    # db_password = models.CharField(verbose_name='Пароль БД')
    # db_iv = models.CharField(verbose_name='Вектор инициализации пароля БД', blank=True, null=True)
    # db_host = models.CharField(verbose_name='Адрес БД', max_length=50)
    # db_port = models.IntegerField(verbose_name='Порт БД')
    is_active = models.BooleanField(verbose_name='Активная школа?', default=True)
    timezone = models.CharField(verbose_name='Часовой пояс', choices=CHOICES)
    photo = models.ForeignKey(Photo, verbose_name='Фотография', related_name='school_photo', on_delete=models.SET_NULL,
                              blank=True, null=True)

    class Meta:
        db_table = "SchoolsDB"
        verbose_name_plural = "Школы"
        ordering = ["-id"]

    def __str__(self):  # указываем название школы в качестве "названия" при отображении экземпляров модели
        return f"(schoolID {self.id}) {self.name}"


# @receiver(post_save, sender=SchoolDB)
# def create_deleted(sender, instance, created, **kwargs):
#     """
#     Устанавливаем обработчик события - при создании экземпляра школы будет создаваться "удаленная" школа (если не существует) для установки значений приудалении внешних ключей
#     """
#     if created and not SchoolDB.objects.filter(name="удаленная школа"):
#         SchoolDB.objects.create(name="удаленная школа")


# class Director(models.Model):
#     objects = models.Manager()
#
#     is_active = models.BooleanField(verbose_name='Активный?', default=True)
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Directors"
#         verbose_name_plural = "Завучи"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.user} | {self.school}"
#
#
# class Teacher(models.Model):
#     objects = models.Manager()
#
#     is_active = models.BooleanField(verbose_name='Активный?', default=True)
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Teachers"
#         verbose_name_plural = "Учителя"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.user} | {self.school}"
#
#
# class FacultativeTeacher(models.Model):
#     objects = models.Manager()
#
#     is_active = models.BooleanField(verbose_name='Активный?', default=True)
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "FacultativeTeachers"
#         verbose_name_plural = "Учителя факультативов"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.user} | {self.school}"
#
#
# class Tutor(models.Model):
#     objects = models.Manager()
#
#     is_active = models.BooleanField(verbose_name='Активный?', default=True)
#     user = models.ForeignKey(User, verbose_name='Пользователь', related_name='tutor_user', on_delete=models.CASCADE)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='tutor_school', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Tutors"
#         verbose_name_plural = "Тьюторы"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.user} | {self.school}"
#
#
# class Parent(models.Model):
#     objects = models.Manager()
#
#     is_active = models.BooleanField(verbose_name='Активный?', default=True)
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Parents"
#         verbose_name_plural = "Родители"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.user} | {self.school}"
#
#
# class Student(models.Model):
#     objects = models.Manager()
#
#     is_active = models.BooleanField(verbose_name='Активный?', default=True)
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Students"
#         verbose_name_plural = "Ученики"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.user} | {self.school}"
#
#
# class Food(models.Model):
#     objects = models.Manager()
#
#     is_active = models.BooleanField(verbose_name='Активный?', default=True)
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Foods"
#         verbose_name_plural = "Операторы питания"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.user} | {self.school}"
#
#
# class ParentChild(models.Model):
#     objects = models.Manager()
#
#     parent = models.ForeignKey(Parent, verbose_name='Родитель', related_name='parent', on_delete=models.CASCADE)
#     child = models.ForeignKey(Student, verbose_name='Ребенок', related_name='child', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "ParentChild"
#         verbose_name_plural = "Родители и дети"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"Родитель: {self.parent} | Ребенок: {self.child}"

#
# class Object(models.Model):
#     objects = models.Manager()
#
#     name = models.CharField(verbose_name='Название', max_length=255)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='object_school', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Objects"
#         verbose_name_plural = "Предметы"
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.name
#
#
# class Cabinet(models.Model):
#     objects = models.Manager()
#
#     name = models.CharField(verbose_name='Название', max_length=255)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='cabinet_school', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Cabinets"
#         verbose_name_plural = "Кабинеты"
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.name
#
#
# class Class(models.Model):
#     objects = models.Manager()
#
#     name = models.CharField(verbose_name='Название', max_length=255)
#     tutor = models.ForeignKey(Tutor, verbose_name='Тьютор', related_name='class_tutor', on_delete=models.CASCADE)
#     cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет', related_name='class_cabinet', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Classes"
#         verbose_name_plural = "Классы"
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.name
#
#
# class Group(models.Model):
#     objects = models.Manager()
#
#     name = models.CharField(verbose_name='Название', max_length=255)
#     school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='group_school', on_delete=models.CASCADE)
#     cls = models.ForeignKey(Class, verbose_name='Класс', related_name='group_class', on_delete=models.CASCADE, blank=True, null=True)
#
#     class Meta:
#         db_table = "Groups"
#         verbose_name_plural = "Группы"
#         ordering = ['-id']
#
#     def __str__(self):
#         if self.cls:
#             return f"{self.name} | {self.cls}"
#         else:
#             return self.name
#
#
# class Lesson(models.Model):
#     objects = models.Manager()
#
#     teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель', related_name='teacher', on_delete=models.CASCADE, blank=True, null=True)
#     teacher = models.ForeignKey(FacultativeTeacher, verbose_name='Преподаватель факультатива', related_name='facultative_teacher', on_delete=models.CASCADE, blank=True, null=True)
#     object = models.ForeignKey(Object, verbose_name='Предмет', related_name='lesson_object', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Lessons"
#         verbose_name_plural = "Уроки"
#         ordering = ['-id']
#
#     def __str__(self):
#         return f"{self.object} | {self.teacher}"
#
#
# class TimeLesson(models.Model):
#     object = models.Manager()
#
#     period = models.CharField(verbose_name='Период действия', max_length=255)
#     lesson1_start = models.TimeField(verbose_name='Начало урока 1')
#     lesson1_end = models.TimeField(verbose_name='Конец урока 1')
#     lesson2_start = models.TimeField(verbose_name='Начало урока 2')
#     lesson2_end = models.TimeField(verbose_name='Конец урока 2')
#     lesson3_start = models.TimeField(verbose_name='Начало урока 3')
#     lesson3_end = models.TimeField(verbose_name='Конец урока 3')
#     lesson4_start = models.TimeField(verbose_name='Начало урока 4')
#     lesson4_end = models.TimeField(verbose_name='Конец урока 4')
#     lesson5_start = models.TimeField(verbose_name='Начало урока 5')
#     lesson5_end = models.TimeField(verbose_name='Конец урока 5')
#     lesson6_start = models.TimeField(verbose_name='Начало урока 6')
#     lesson6_end = models.TimeField(verbose_name='Конец урока 6')
#     lesson7_start = models.TimeField(verbose_name='Начало урока 7')
#     lesson7_end = models.TimeField(verbose_name='Конец урока 7')
#     lesson8_start = models.TimeField(verbose_name='Начало урока 8', blank=True, null=True)
#     lesson8_end = models.TimeField(verbose_name='Конец урока 8', blank=True, null=True)
#     lesson9_start = models.TimeField(verbose_name='Начало урока 9', blank=True, null=True)
#     lesson9_end = models.TimeField(verbose_name='Конец урока 9', blank=True, null=True)
#     lesson10_start = models.TimeField(verbose_name='Начало урока 10', blank=True, null=True)
#     lesson10_end = models.TimeField(verbose_name='Конец урока 10', blank=True, null=True)
#
#     class Meta:
#         db_table = "TimeLessons"
#         verbose_name_plural = "Время уроков"
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.period
#
#
# class Schedule(models.Model):
#     CHOICES = [
#         (1, 'Урок 1'),
#         (2, 'Урок 2'),
#         (3, 'Урок 3'),
#         (4, 'Урок 4'),
#         (5, 'Урок 5'),
#         (6, 'Урок 6'),
#         (7, 'Урок 7'),
#         (8, 'Урок 8'),
#         (9, 'Урок 9'),
#         (10, 'Урок 10'),
#     ]
#
#     object = models.Manager()
#
#     date = models.DateField(verbose_name='Дата')
#     number = models.IntegerField(verbose_name='Номер урока', choices=CHOICES)
#     start = models.TimeField(verbose_name='Измененное начало урока', blank=True, null=True)
#     end = models.TimeField(verbose_name='Измененное завершение урока', blank=True, null=True)
#     comment = models.CharField(verbose_name='Комментарий к уроку', max_length=255, blank=True, null=True)
#     replace_comment = models.CharField(verbose_name='Комментарий к замене урока', max_length=255, blank=True, null=True)
#     is_cancelled = models.BooleanField(verbose_name='Отмена урока', default=False)
#     cancelled_comment = models.CharField(verbose_name='Комментарий к отмене урока', max_length=255, blank=True, null=True)
#     lesson = models.ForeignKey(Lesson, verbose_name='Урок', related_name='lesson', on_delete=models.CASCADE)
#     lesson_replace = models.ForeignKey(Lesson, verbose_name='Замена урока', related_name='lesson_replace', on_delete=models.CASCADE, blank=True, null=True)
#     student = models.ForeignKey(Student, verbose_name='Ученик', related_name='schedule_student', on_delete=models.CASCADE, blank=True, null=True)
#     group = models.ForeignKey(Group, verbose_name='Группа', related_name='schedule_group', on_delete=models.CASCADE, blank=True, null=True)
#     cls = models.ForeignKey(Class, verbose_name='Класс', related_name='schedule_class', on_delete=models.CASCADE, blank=True, null=True)
#     cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет', related_name='schedule_cabinet', on_delete=models.CASCADE, blank=True, null=True)
#     time_lessons = models.ForeignKey(TimeLesson, verbose_name='Время уроков', related_name='schedule_time', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "Schedules"
#         verbose_name_plural = "Уроки для расписания"
#         ordering = ['-id']
#
#     def __str__(self):
#         if self.lesson_replace and self.cabinet:
#             return f"№ {self.number} - {self.date} | {self.lesson_replace} -> {self.lesson} | {self.cabinet}"
#         elif self.lesson_replace and not self.cabinet:
#             return f"№ {self.number} - {self.date} | {self.lesson_replace} -> {self.lesson}"
#         else:
#             return f"№ {self.number} - {self.date} | {self.lesson}"
