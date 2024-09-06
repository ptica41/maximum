from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Photo, User, SchoolDB #  Object, Cabinet, Class, Group, Lesson, TimeLesson, Schedule
from oneC.models import Partner1C, ParentChild1C
from roles.models import Director, Teacher, FacultativeTeacher, Tutor, Parent, Student, Food, ParentChild
from schedules.models import Object, Cabinet, Class, Group, Lesson, TimeLesson, Schedule, StudentGroup, StudentClass

from .serializers import encrypt_pswrd




class UserAdmin(BaseUserAdmin):
    """
    Переопределяем стандартный класс пользователей, чтобы пароль хэшировался перед записью (ТОЛЬКО в админке бэкенда)
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"),
         {"fields": ("name", "surname", "middle_name", "photo", "male", "birthday", "phone", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "name", "surname", "middle_name", "date_joined", "last_login", "is_active")
    list_filter = ("is_superuser", "is_active", "groups")
    search_fields = ("username", "name", "surname", "email")


# class SchoolDBAdmin(admin.ModelAdmin):
#     """
#     Переопределяем класс Школ, для шифрования пароля БД школы
#     """
#
#     def save_model(self, request, obj, form, change, **kwargs):
#         if SchoolDB.objects.filter(id=obj.id).exists():  # случай, когда объект школы редактируется
#             school = SchoolDB.objects.get(id=obj.id)
#             if school.db_password != obj.db_password:
#                 obj.db_password, obj.db_iv = encrypt_pswrd(
#                     obj.db_password)  # шифруем пароль, а также записываем значение вектора инициализации для дешифрования
#             else:
#                 obj.db_iv = school.db_iv  # защита от случайного изменения вектора инициализации без смены пароля
#         else:  # случай, когда объект школы создается
#             obj.db_password, obj.db_iv = encrypt_pswrd(
#                 obj.db_password)  # шифруем пароль, а также записываем значение вектора инициализации для дешифрования
#
#         super().save_model(request, obj, form, change)


# Регистрируем модели в админке
admin.site.register(User, UserAdmin)
admin.site.register(SchoolDB)
admin.site.register(Director)
admin.site.register(Teacher)
admin.site.register(FacultativeTeacher)
admin.site.register(Tutor)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Food)
admin.site.register(ParentChild)
admin.site.register(Photo)
admin.site.register(Partner1C)
admin.site.register(ParentChild1C)
admin.site.register(Object)
admin.site.register(Cabinet)
admin.site.register(Class)
admin.site.register(StudentClass)
admin.site.register(Group)
admin.site.register(StudentGroup)
admin.site.register(Lesson)
admin.site.register(TimeLesson)
admin.site.register(Schedule)
