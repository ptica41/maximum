import datetime
import pytz

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


from rest_framework import serializers

from main_app.models import User, SchoolDB
from roles.models import Tutor, Teacher, FacultativeTeacher, Student



class Object(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название', max_length=255)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='object_school', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "Objects"
        verbose_name_plural = "Предметы"
        ordering = ['-id']

    def __str__(self):
        return f"(objectID {self.id}) {self.name} | {self.school}"


class Cabinet(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название', max_length=255)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='cabinet_school', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "Cabinets"
        verbose_name_plural = "Кабинеты"
        ordering = ['-id']

    def __str__(self):
        return f"(cabinetID {self.id}) {self.name} | {self.school}"


class Class(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название', max_length=255)
    tutor = models.ForeignKey(Tutor, verbose_name='Тьютор', related_name='class_tutor', on_delete=models.SET_NULL, blank=True, null=True)
    cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет', related_name='class_cabinet', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "Classes"
        verbose_name_plural = "Классы"
        ordering = ['-id']

    def __str__(self):
        return f"(classID {self.id}) {self.name} | {self.cabinet}"


class StudentClass(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    cls = models.ForeignKey(Class, verbose_name='Класс', related_name='cls_student', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Ученик', related_name='student_cls', on_delete=models.CASCADE)

    class Meta:
        db_table = "StudentClasses"
        verbose_name_plural = "Ученики и классы"
        ordering = ['-id']

    def __str__(self):
        return f"(studentClassID {self.id}) Ученик: {self.student} | Класс: {self.cls}"


class Group(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название', max_length=255)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='group_school', on_delete=models.SET_NULL, blank=True, null=True)
    cls = models.ForeignKey(Class, verbose_name='Класс', related_name='group_class', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "Groups"
        verbose_name_plural = "Группы"
        ordering = ['-id']

    def __str__(self):
        if self.cls:
            return f"(groupID {self.id}) {self.name} | {self.cls}"
        else:
            return f"(groupID {self.id}) {self.name} | {self.school}"


class StudentGroup(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, verbose_name='Класс', related_name='group_student', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Ученик', related_name='student_group', on_delete=models.CASCADE)

    class Meta:
        db_table = "StudentGroups"
        verbose_name_plural = "Ученики и группы"
        ordering = ['-id']

    def __str__(self):
        return f"(studentGroupID {self.id}) Ученик: {self.student} | Группа: {self.group}"


class Lesson(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, verbose_name='Учитель', related_name='teacher', on_delete=models.SET_NULL, blank=True, null=True)
    facultative_teacher = models.ForeignKey(FacultativeTeacher, verbose_name='Учитель факультатива', related_name='facultative_teacher', on_delete=models.SET_NULL, blank=True, null=True)
    object = models.ForeignKey(Object, verbose_name='Предмет', related_name='lesson_object', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "Lessons"
        verbose_name_plural = "Уроки"
        ordering = ['-id']

    def __str__(self):
        if self.teacher:
            return f"(lessonID {self.id}) {self.object} | {self.teacher}"
        else:
            return f"(lessonID {self.id}) {self.object} | {self.facultative_teacher}"


class TimeLesson(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    period = models.CharField(verbose_name='Период действия', max_length=255)
    lesson1_start = models.TimeField(verbose_name='Начало урока 1')
    lesson1_end = models.TimeField(verbose_name='Конец урока 1')
    lesson2_start = models.TimeField(verbose_name='Начало урока 2')
    lesson2_end = models.TimeField(verbose_name='Конец урока 2')
    lesson3_start = models.TimeField(verbose_name='Начало урока 3')
    lesson3_end = models.TimeField(verbose_name='Конец урока 3')
    lesson4_start = models.TimeField(verbose_name='Начало урока 4')
    lesson4_end = models.TimeField(verbose_name='Конец урока 4')
    lesson5_start = models.TimeField(verbose_name='Начало урока 5')
    lesson5_end = models.TimeField(verbose_name='Конец урока 5')
    lesson6_start = models.TimeField(verbose_name='Начало урока 6')
    lesson6_end = models.TimeField(verbose_name='Конец урока 6')
    lesson7_start = models.TimeField(verbose_name='Начало урока 7', blank=True, null=True)
    lesson7_end = models.TimeField(verbose_name='Конец урока 7', blank=True, null=True)
    lesson8_start = models.TimeField(verbose_name='Начало урока 8', blank=True, null=True)
    lesson8_end = models.TimeField(verbose_name='Конец урока 8', blank=True, null=True)
    lesson9_start = models.TimeField(verbose_name='Начало урока 9', blank=True, null=True)
    lesson9_end = models.TimeField(verbose_name='Конец урока 9', blank=True, null=True)
    lesson10_start = models.TimeField(verbose_name='Начало урока 10', blank=True, null=True)
    lesson10_end = models.TimeField(verbose_name='Конец урока 10', blank=True, null=True)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='time_lesson_school', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "TimeLessons"
        verbose_name_plural = "Время уроков"
        ordering = ['-id']

    def __str__(self):
        return f"(timeLessonID {self.id}) {self.period}"


class Schedule(models.Model):
    CHOICES = [
        (1, 'Урок 1'),
        (2, 'Урок 2'),
        (3, 'Урок 3'),
        (4, 'Урок 4'),
        (5, 'Урок 5'),
        (6, 'Урок 6'),
        (7, 'Урок 7'),
        (8, 'Урок 8'),
        (9, 'Урок 9'),
        (10, 'Урок 10'),
    ]

    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name='Номер урока', choices=CHOICES, blank=True, null=True)  # указывается в случае post запроса и выбора шаблонного времени расписания (для изменения будущих расписаний в случае изменения шаблонного времени урока)
    start = models.DateTimeField(verbose_name='Измененное начало урока')
    end = models.DateTimeField(verbose_name='Измененное завершение урока')
    comment = models.CharField(verbose_name='Комментарий к уроку', max_length=255, blank=True, null=True)
    replace_comment = models.CharField(verbose_name='Комментарий к замене урока', max_length=255, blank=True, null=True)
    is_cancelled = models.BooleanField(verbose_name='Отмена урока', default=False)
    cancelled_comment = models.CharField(verbose_name='Комментарий к отмене урока', max_length=255, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name='Урок', related_name='lesson', on_delete=models.SET_NULL, blank=True, null=True)
    lesson_replace = models.ForeignKey(Lesson, verbose_name='Замена урока', related_name='lesson_replace', on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, verbose_name='Ученик', related_name='schedule_student', on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(Group, verbose_name='Группа', related_name='schedule_group', on_delete=models.SET_NULL, blank=True, null=True)
    cls = models.ForeignKey(Class, verbose_name='Класс', related_name='schedule_class', on_delete=models.SET_NULL, blank=True, null=True)
    cabinet = models.ForeignKey(Cabinet, verbose_name='Кабинет', related_name='schedule_cabinet', on_delete=models.SET_NULL, blank=True, null=True)
    time_lesson = models.ForeignKey(TimeLesson, verbose_name='Время уроков', related_name='schedule_time', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "Schedules"
        verbose_name_plural = "Уроки для расписания"
        ordering = ['-id']

    def __str__(self):
        if self.lesson_replace and self.cabinet:
            return f"(scheduleID {self.id}) № {self.number} - {self.start}-{self.end} | {self.lesson} -> {self.lesson_replace} | {self.cabinet}"
        elif self.lesson_replace and not self.cabinet:
            return f"(scheduleID {self.id}) № {self.number} - {self.start}-{self.end} | {self.lesson} -> {self.lesson_replace}"
        else:
            return f"(scheduleID {self.id}) № {self.number} - {self.start}-{self.end} | {self.lesson}"


@receiver(post_save, sender=TimeLesson)
def edit_time_lessons(sender, instance, created, **kwargs):
    """
    При изменении экземпляра модели TimeLesson изменяем значения полей start и end (которые еще не прошли) в связанных экземплярах модели Schedule
    """
    if not created:
        schedules = Schedule.objects.filter(time_lesson=instance)
        now = datetime.datetime.now().date()

        for schedule in schedules:
            if schedule.number:
                if schedule.start.date() >= now:
                    schedule.start = schedule.start.strftime("%Y-%m-%d") + ' ' + getattr(instance, f"lesson{schedule.number}_start").strftime("%H:%M:%S") + instance.school.timezone
                    schedule.end = schedule.end.strftime("%Y-%m-%d") + ' ' + getattr(instance, f"lesson{schedule.number}_end").strftime("%H:%M:%S") + instance.school.timezone
                    print(schedule.start)
                    schedule.save()
