from django.db import models

from main_app.models import User, SchoolDB


class Director(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный?', default=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)

    class Meta:
        db_table = "Directors"
        verbose_name_plural = "Завучи"
        ordering = ['-id']

    def __str__(self):
        return f"(directorID {self.id}) {self.user} | {self.school}"


class Teacher(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный?', default=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)

    class Meta:
        db_table = "Teachers"
        verbose_name_plural = "Учителя"
        ordering = ['-id']

    def __str__(self):
        return f"(teacherID {self.id}) {self.user} | {self.school}"


class FacultativeTeacher(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный?', default=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)

    class Meta:
        db_table = "FacultativeTeachers"
        verbose_name_plural = "Учителя факультативов"
        ordering = ['-id']

    def __str__(self):
        return f"(facultativeTeacherID {self.id}) {self.user} | {self.school}"


class Tutor(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный?', default=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='tutor_user', on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', related_name='tutor_school', on_delete=models.CASCADE)

    class Meta:
        db_table = "Tutors"
        verbose_name_plural = "Тьюторы"
        ordering = ['-id']

    def __str__(self):
        return f"(tutorID {self.id}) {self.user} | {self.school}"


class Parent(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный?', default=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)

    class Meta:
        db_table = "Parents"
        verbose_name_plural = "Родители"
        ordering = ['-id']

    def __str__(self):
        return f"(parentID {self.id}) {self.user} | {self.school}"


class Student(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный?', default=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)

    class Meta:
        db_table = "Students"
        verbose_name_plural = "Ученики"
        ordering = ['-id']

    def __str__(self):
        return f"(studentID {self.id}) {self.user} | {self.school}"


class Food(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный?', default=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDB, verbose_name='Школа', on_delete=models.CASCADE)

    class Meta:
        db_table = "Foods"
        verbose_name_plural = "Операторы питания"
        ordering = ['-id']

    def __str__(self):
        return f"(foodID {self.id}) {self.user} | {self.school}"


class ParentChild(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Parent, verbose_name='Родитель', related_name='parent', on_delete=models.CASCADE)
    child = models.ForeignKey(Student, verbose_name='Ребенок', related_name='child', on_delete=models.CASCADE)

    class Meta:
        db_table = "ParentChild"
        verbose_name_plural = "Родители и дети"
        ordering = ['-id']

    def __str__(self):
        return f"(parentChildID {self.id}) Родитель: {self.parent} | Ребенок: {self.child}"
