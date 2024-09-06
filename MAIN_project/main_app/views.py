import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.utils import timezone

from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed as AuthFailed

from .serializers import UserAdminSerializer, UserSerializer, SchoolSerializer, PhotoSerializer
from .models import Photo, User, SchoolDB  # , Object, Cabinet, Class, Group, Lesson, TimeLesson, Schedule
from roles.models import Director, Teacher, FacultativeTeacher, Tutor, Parent, Student, Food, ParentChild
from roles.serializers import DirectorSerializer, TeacherSerializer, FacultativeTeacherSerializer, TutorSerializer, \
    ParentSerializer, StudentSerializer, FoodSerializer, ParentChildSerializer

import os


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            user = super().authenticate(request)
        except InvalidToken:
            raise AuthenticationFailed([{"title": "accessInvalid", "description": "недействительный access токен"}])
        except AuthFailed:
            raise AuthenticationFailed([{"title": "inactiveUser", "description": "Неактивный пользователь"}])
        return user


class IsActive(IsAuthenticated):
    """
    Переопределение класса проверки аутентификации.
    Если пользователь аутентифицирован - обновляем поле last_login
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            raise AuthenticationFailed([{"title": "invalidAuthentication", "description": "Пользователь не аутентифицирован"}])
        if not request.user.is_active:
            raise AuthenticationFailed([{"title": "inactiveUser", "description": "Неактивный пользователь"}])
        request.user.last_login = datetime.datetime.now(tz=timezone.utc)
        request.user.save()
        return True


def get_user_schools(user, role_is_active=True, school_is_active=True):
    """
    Получаем список школ юзера по ролям
    """
    schools = []
    if Director.objects.filter(user=user, is_active=role_is_active, school__is_active=school_is_active).exists():
        for director in Director.objects.filter(user=user, is_active=role_is_active,
                                                school__is_active=school_is_active).values('school'):
            if director not in schools:
                schools.append(director)
    if Teacher.objects.filter(user=user, is_active=role_is_active, school__is_active=school_is_active).exists():
        for teacher in Teacher.objects.filter(user=user, is_active=role_is_active,
                                              school__is_active=school_is_active).values('school'):
            if teacher not in schools:
                schools.append(teacher)
    if FacultativeTeacher.objects.filter(user=user, is_active=role_is_active,
                                         school__is_active=school_is_active).exists():
        for fac_teacher in FacultativeTeacher.objects.filter(user=user, is_active=role_is_active,
                                                             school__is_active=school_is_active).values('school'):
            if fac_teacher not in schools:
                schools.append(fac_teacher)
    if Tutor.objects.filter(user=user, is_active=role_is_active, school__is_active=school_is_active).exists():
        for tutor in Tutor.objects.filter(user=user, is_active=role_is_active,
                                          school__is_active=school_is_active).values('school'):
            if tutor not in schools:
                schools.append(tutor)
    if Parent.objects.filter(user=user, is_active=role_is_active, school__is_active=school_is_active).exists():
        for parent in Parent.objects.filter(user=user, is_active=role_is_active,
                                            school__is_active=school_is_active).values('school'):
            if parent not in schools:
                schools.append(parent)
    if Student.objects.filter(user=user, is_active=role_is_active, school__is_active=school_is_active).exists():
        for student in Student.objects.filter(user=user, is_active=role_is_active,
                                              school__is_active=school_is_active).values('school'):
            if student not in schools:
                schools.append(student)
    if Food.objects.filter(user=user, is_active=role_is_active, school__is_active=school_is_active).exists():
        for food in Food.objects.filter(user=user, is_active=role_is_active, school__is_active=school_is_active).values(
                'school'):
            if food not in schools:
                schools.append(food)
    return schools


def get_school_users(school, school_is_active=True, role_is_active=True):
    """
    Получаем список всех активных пользователей школы c ролями
    """
    users = []
    if school_is_active:
        if Director.objects.filter(user__is_active=True, is_active=role_is_active, school=school).exists():
            for director in Director.objects.filter(user__is_active=True, is_active=role_is_active,
                                                    school=school).values('user'):
                if director not in users:
                    users.append(director)
        if Teacher.objects.filter(user__is_active=True, is_active=role_is_active, school=school).exists():
            for teacher in Teacher.objects.filter(user__is_active=True, is_active=role_is_active, school=school).values(
                    'user'):
                if teacher not in users:
                    users.append(teacher)
        if FacultativeTeacher.objects.filter(user__is_active=True, is_active=role_is_active, school=school).exists():
            for fac_teacher in FacultativeTeacher.objects.filter(user__is_active=True, is_active=role_is_active,
                                                                 school=school).values('user'):
                if fac_teacher not in users:
                    users.append(fac_teacher)
        if Tutor.objects.filter(user__is_active=True, is_active=role_is_active, school=school).exists():
            for tutor in Tutor.objects.filter(user__is_active=True, is_active=role_is_active, school=school).values(
                    'user'):
                if tutor not in users:
                    users.append(tutor)
        if Parent.objects.filter(user__is_active=True, is_active=role_is_active, school=school).exists():
            for parent in Parent.objects.filter(user__is_active=True, is_active=role_is_active, school=school).values(
                    'user'):
                if parent not in users:
                    users.append(parent)
        if Student.objects.filter(user__is_active=True, is_active=role_is_active, school=school).exists():
            for student in Student.objects.filter(user__is_active=True, is_active=role_is_active, school=school).values(
                    'user'):
                if student not in users:
                    users.append(student)
        if Food.objects.filter(user__is_active=True, is_active=role_is_active, school=school).exists():
            for food in Food.objects.filter(user__is_active=True, is_active=role_is_active, school=school).values(
                    'user'):
                if food not in users:
                    users.append(food)
    else:
        raise serializers.ValidationError("Wrong ID school or school isn't active")

    return users


def get_school_users_to_admin(school, role_is_active=True):
    """
    Получаем список всех пользователей любой школы c любыми ролями (для суперпользователя)
    """
    users = []
    if Director.objects.filter(school=school, is_active=role_is_active).exists():
        for director in Director.objects.filter(school=school, is_active=role_is_active).values('user'):
            if director not in users:
                users.append(director)
    if Teacher.objects.filter(school=school, is_active=role_is_active).exists():
        for teacher in Teacher.objects.filter(school=school, is_active=role_is_active).values('user'):
            if teacher not in users:
                users.append(teacher)
    if FacultativeTeacher.objects.filter(school=school, is_active=role_is_active).exists():
        for fac_teacher in FacultativeTeacher.objects.filter(school=school, is_active=role_is_active).values('user'):
            if fac_teacher not in users:
                users.append(fac_teacher)
    if Tutor.objects.filter(school=school, is_active=role_is_active).exists():
        for tutor in Tutor.objects.filter(school=school, is_active=role_is_active).values('user'):
            if tutor not in users:
                users.append(tutor)
    if Parent.objects.filter(school=school, is_active=role_is_active).exists():
        for parent in Parent.objects.filter(school=school, is_active=role_is_active).values('user'):
            if parent not in users:
                users.append(parent)
    if Student.objects.filter(school=school, is_active=role_is_active).exists():
        for student in Student.objects.filter(school=school, is_active=role_is_active).values('user'):
            if student not in users:
                users.append(student)
    if Food.objects.filter(school=school, is_active=role_is_active).exists():
        for food in Food.objects.filter(school=school, is_active=role_is_active).values('user'):
            if food not in users:
                users.append(food)
    return users


class WhoAmIView(APIView):
    """
    Получение данных пользователя (профиль, школы, роли) по токену авторизации
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)
    response = {}

    def get(self, request):
        self.response['roles'] = {}
        self.response['schools'] = []  # список для записи данных школ (для очищения перед каждым запросом)
        self.response['children'] = []

        serializer = UserSerializer(instance=request.user)
        self.response['user'] = serializer.data

        if Director.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            zav = Director.objects.filter(user=request.user, is_active=True, school__is_active=True)
            serializer = DirectorSerializer(instance=zav, many=True)
            self.response['roles']['director'] = serializer.data
            for i in zav:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.response['schools']:
                    self.response['schools'].append(serializer.data)

        if Teacher.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            teacher = Teacher.objects.filter(user=request.user, is_active=True, school__is_active=True)
            serializer = TeacherSerializer(instance=teacher, many=True)
            self.response['roles']['teacher'] = serializer.data
            for i in teacher:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.response['schools']:
                    self.response['schools'].append(serializer.data)

        if FacultativeTeacher.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            facultative_teacher = FacultativeTeacher.objects.filter(user=request.user, is_active=True,
                                                                    school__is_active=True)
            serializer = FacultativeTeacherSerializer(instance=facultative_teacher, many=True)
            self.response['roles']['facultative_teacher'] = serializer.data
            for i in facultative_teacher:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.response['schools']:
                    self.response['schools'].append(serializer.data)

        if Tutor.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            tutor = Tutor.objects.filter(user=request.user, is_active=True, school__is_active=True)
            serializer = TutorSerializer(instance=tutor, many=True)
            self.response['roles']['tutor'] = serializer.data
            for i in tutor:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.response['schools']:
                    self.response['schools'].append(serializer.data)

        if Parent.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            parent = Parent.objects.filter(user=request.user, is_active=True, school__is_active=True)
            serializer = ParentSerializer(instance=parent, many=True)
            self.response['roles']['parent'] = serializer.data
            for i in parent:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.response['schools']:
                    self.response['schools'].append(serializer.data)

        if Student.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            student = Student.objects.filter(user=request.user, is_active=True, school__is_active=True)
            serializer = StudentSerializer(instance=student, many=True)
            self.response['roles']['student'] = serializer.data
            for i in student:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.response['schools']:
                    self.response['schools'].append(serializer.data)

        if Food.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            food = Food.objects.filter(user=request.user, is_active=True, school__is_active=True)
            serializer = FoodSerializer(instance=food, many=True)
            self.response['roles']['food'] = serializer.data
            for i in food:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.response['schools']:
                    self.response['schools'].append(serializer.data)

        if SchoolDB.objects.filter(is_active=True).exists():
            for school in SchoolDB.objects.filter(is_active=True):
                if Parent.objects.filter(user=request.user, school=school).exists():
                    for parent in Parent.objects.filter(user=request.user, school=school):
                        for child in ParentChild.objects.filter(parent=parent, child__user__is_active=True):
                            serializer = UserSerializer(instance=child.child.user)
                            self.response['children'].append(serializer.data)

        return Response(self.response, status=status.HTTP_200_OK)


class MyChildrenAPIView(APIView):
    """
    Получение данных профилей детей по токену авторизации и id (необязательно) школы
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request):
        data = []
        if 'HTTP_SCHOOL' in request.META.keys():
            try:
                school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")
            if Parent.objects.filter(user=request.user, is_active=True, school=school).exists() and school.is_active:
                for parent in Parent.objects.filter(user=request.user, is_active=True, school=school):
                    for child in ParentChild.objects.filter(parent=parent, child__user__is_active=True, child__is_active=True, child__school=school):
                        serializer = UserSerializer(instance=child.child.user)
                        if serializer.data not in data:
                            data.append(serializer.data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                raise serializers.ValidationError("User isn't a active parent at this school or school isn't active")
        else:
            if Parent.objects.filter(user=request.user, is_active=True).exists():
                for parent in Parent.objects.filter(user=request.user, is_active=True):
                    for child in ParentChild.objects.filter(parent=parent, child__user__is_active=True, child__is_active=True):
                        serializer = UserSerializer(instance=child.child.user)
                        if serializer.data not in data:
                            data.append(serializer.data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                raise serializers.ValidationError("User isn't a active parent at this school or school isn't active")


class UploadPhotoAPIView(APIView):
    """
    Загрузка фото в хранилище
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def post(self, request, *args, **kwargs):
        photo = request.data
        serializer = PhotoSerializer(data=photo)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoAPIView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        """
        Получение фото по id
        """
        try:
            photo = Photo.objects.get(id=kwargs.get('pk'))
            photo_path = os.path.join(settings.MEDIA_ROOT, photo.photo.name)
            return FileResponse(open(photo_path, 'rb'), content_type='image/jpeg')

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        """
        Важно! id фотографии должно принадлежать только одной сущности!
        Фотография и миниатюра с переданным id удаляются, в ответ приходят фотография с миниатюрой с новым id (такая реализация для нужного кэширования фотографий на фронте)
        Новый id заменяет старый в нужной сущности (пользователь или школа)
        """
        try:
            photo = Photo.objects.get(id=kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

        if request.user.is_superuser:
            photo_new = request.data
            serializer = PhotoSerializer(data=photo_new)
            if serializer.is_valid():
                serializer.save()
            if User.objects.filter(photo=photo).exists():
                user = User.objects.get(photo=photo)
                user.photo = Photo.objects.get(id=serializer.data['id'])
                user.save()
            elif SchoolDB.objects.filter(photo=photo).exists():
                school = SchoolDB.objects.get(photo=photo)
                school.photo = Photo.objects.get(id=serializer.data['id'])
                school.save()
            photo.delete()

        elif Director.objects.filter(user=request.user).exists():
            photo_new = request.data
            serializer = PhotoSerializer(data=photo_new)
            if User.objects.filter(photo=photo).exists() and request.user == User.objects.get(photo=photo):
                if serializer.is_valid():
                    serializer.save()
                user = User.objects.get(photo=photo)
                user.photo = Photo.objects.get(id=serializer.data['id'])
                user.save()
            elif Director.objects.filter(user=request.user, school__photo=photo).exists():
                if serializer.is_valid():
                    serializer.save()
                school = SchoolDB.objects.get(photo=photo)
                school.photo = Photo.objects.get(id=serializer.data['id'])
                school.save()
            else:
                raise serializers.ValidationError("permission denied")
            photo.delete()

        elif User.objects.filter(photo=photo).exists() and request.user == User.objects.get(photo=photo):
            photo_new = request.data
            serializer = PhotoSerializer(data=photo_new)
            if serializer.is_valid():
                serializer.save()
            user = User.objects.get(photo=photo)
            user.photo = Photo.objects.get(id=serializer.data['id'])
            user.save()
            photo.delete()

        else:
            raise serializers.ValidationError("permission denied")

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Удаление фото и миниатюры по id
        """
        try:
            photo = Photo.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                photo.delete()
            elif Director.objects.filter(user=request.user).exists():
                if User.objects.filter(photo=photo).exists() and request.user == User.objects.get(photo=photo):
                    photo.delete()
                elif Director.objects.filter(user=request.user, school__photo=photo).exists():
                    photo.delete()
                else:
                    raise serializers.ValidationError("permission denied")
            elif User.objects.filter(photo=photo).exists() and request.user == User.objects.get(photo=photo):
                photo.delete()
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class PhotoMinAPIView(APIView):
    """
    Получение миниатюры по id
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            photo = Photo.objects.get(id=kwargs.get('pk'))
            photo_path = os.path.join(settings.MEDIA_ROOT, photo.photo_min.name)
            return FileResponse(open(photo_path, 'rb'), content_type='image/jpeg')

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")


class UsersAPIView(GenericAPIView):
    """
    Получение список пользователей
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['surname']
    ordering_fields = '__all__'
    filterset_fields = {
        "is_active": ["exact", ],
        "role_is_active": ["exact", ],
        "date_joined": ["lte", "gte"],
        "last_login": ["lte", "gte"]
    }

    def get(self, request):
        list_users = []
        if 'HTTP_SCHOOL' in request.META.keys():
            try:
                school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])

                if request.user.is_superuser:
                    _users = get_school_users_to_admin(school, role_is_active=False)  # получаем список всех пользователей с неактивными ролями в любой школе
                    for _user in _users:
                        user = User.objects.get(id=_user.get('user'))
                        user.role_is_active = False  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if _user.get('user') not in list_users:
                            list_users.append(_user.get('user'))

                    _users = get_school_users_to_admin(school)  # получаем список всех пользователей с активными ролями в любой школе
                    for _user in _users:
                        user = User.objects.get(id=_user.get('user'))
                        user.role_is_active = True  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if _user.get('user') not in list_users:
                            list_users.append(_user.get('user'))

                    users = User.objects.filter(id__in=list_users)
                    filter_users = self.filter_queryset(users)
                    page_users = self.paginate_queryset(filter_users)
                    serializer = UserSerializer(instance=page_users, many=True)
                    return self.get_paginated_response(serializer.data)

                elif Director.objects.filter(user=request.user, is_active=True, school=school).exists() and school.is_active:
                    _users = get_school_users(school, role_is_active=False)  # получаем список активных пользователей с неактивными ролями в активной школе
                    for _user in _users:
                        user = User.objects.get(id=_user.get('user'))
                        user.role_is_active = False  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if _user.get('user') not in list_users:
                            list_users.append(_user.get('user'))

                    _users = get_school_users(school)  # получаем список активных пользователей с активными ролями в активной школе
                    for _user in _users:
                        user = User.objects.get(id=_user.get('user'))
                        user.role_is_active = True  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if _user.get('user') not in list_users:
                            list_users.append(_user.get('user'))

                    users = User.objects.filter(id__in=list_users)
                    filter_users = self.filter_queryset(users)
                    page_users = self.paginate_queryset(filter_users)
                    serializer = UserSerializer(instance=page_users, many=True)
                    return self.get_paginated_response(serializer.data)

                elif school.is_active:
                    if school.id in [i.get('school') for i in get_user_schools(request.user)]:
                        _users = get_school_users(school)  # получаем список активных пользователей с активными ролями в активной школе
                        for _user in _users:
                            user = User.objects.get(id=_user.get('user'))
                            user.role_is_active = True  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                            user.save()
                            if _user.get('user') not in list_users:
                                list_users.append(_user.get('user'))

                        users = User.objects.filter(id__in=list_users)
                        filter_users = self.filter_queryset(users)
                        page_users = self.paginate_queryset(filter_users)
                        serializer = UserSerializer(instance=page_users, many=True)
                        return self.get_paginated_response(serializer.data)
                    else:
                        raise serializers.ValidationError("Permission denied")
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")
        else:
            if request.user.is_superuser:
                _users = User.objects.all()
                filter_users = self.filter_queryset(_users)
                page_users = self.paginate_queryset(filter_users)
                serializer = UserAdminSerializer(instance=page_users, many=True)
            elif Director.objects.filter(user=request.user, is_active=True).exists():
                _users = User.objects.filter(is_active=True, is_superuser=False)
                filter_users = self.filter_queryset(_users)
                page_users = self.paginate_queryset(filter_users)
                serializer = UserSerializer(instance=page_users, many=True)
            else:
                schools = get_user_schools(request.user)
                for school in schools:
                    ids = get_school_users(SchoolDB.objects.get(id=school.get('school')))
                    for id in ids:
                        if id.get('user') not in list_users:
                            list_users.append(id.get('user'))
                _users = User.objects.filter(id__in=list_users)
                filter_users = self.filter_queryset(_users)
                page_users = self.paginate_queryset(filter_users)
                serializer = UserSerializer(instance=page_users, many=True)
            return self.get_paginated_response(serializer.data)

    def post(self, request):
        if request.user.is_superuser:
            data = request.data
            serializer = UserAdminSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class UserAPIView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = UserAdminSerializer(instance=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif Director.objects.filter(user=request.user, is_active=True).exists():
                for director in Director.objects.filter(user=request.user, is_active=True):
                    if director.school.id in [i.get('school') for i in get_user_schools(user)]:
                        serializer = UserSerializer(instance=user)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                raise serializers.ValidationError("Permission denied")
            elif [x for x in get_user_schools(request.user) if x in get_user_schools(user)] and user.is_active:
                serializer = UserSerializer(instance=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = UserAdminSerializer(instance=user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.user == user:
                serializer = UserSerializer(instance=user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class UserRolesAPIView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)
    response = {}

    def get(self, request, *args, **kwargs):
        self.response['roles'] = {}

        try:
            user = User.objects.get(id=kwargs.get('pk'))
            if 'HTTP_SCHOOL' in request.META.keys():
                try:
                    school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])
                except ObjectDoesNotExist:
                    raise serializers.ValidationError("Wrong school ID")
                if request.user.is_superuser:
                    if Director.objects.filter(user=user, school=school).exists():
                        serializer = DirectorSerializer(instance=Director.objects.filter(user=user, school=school), many=True)
                        self.response['roles']['director'] = serializer.data
                    if Teacher.objects.filter(user=user, school=school).exists():
                        serializer = TeacherSerializer(instance=Teacher.objects.filter(user=user, school=school), many=True)
                        self.response['roles']['teacher'] = serializer.data
                    if FacultativeTeacher.objects.filter(user=user, school=school).exists():
                        serializer = FacultativeTeacherSerializer(instance=FacultativeTeacher.objects.filter(user=user, school=school), many=True)
                        self.response['roles']['facultative_teacher'] = serializer.data
                    if Tutor.objects.filter(user=user, school=school).exists():
                        serializer = TutorSerializer(instance=Tutor.objects.filter(user=user, school=school), many=True)
                        self.response['roles']['tutor'] = serializer.data
                    if Parent.objects.filter(user=user, school=school).exists():
                        serializer = ParentSerializer(instance=Parent.objects.filter(user=user, school=school), many=True)
                        self.response['roles']['parent'] = serializer.data
                    if Student.objects.filter(user=user, school=school).exists():
                        serializer = StudentSerializer(instance=Student.objects.filter(user=user, school=school), many=True)
                        self.response['roles']['student'] = serializer.data
                    if Food.objects.filter(user=user, school=school).exists():
                        serializer = FoodSerializer(instance=Food.objects.filter(user=user, school=school), many=True)
                        self.response['roles']['food'] = serializer.data
                    if ParentChild.objects.filter(parent__user=user, parent__school=school, child__school=school).exists() or ParentChild.objects.filter(child__user=user, parent__school=school, child__school=school).exists():
                        serializer = ParentChildSerializer(instance=ParentChild.objects.filter(parent__user=user, parent__school=school, child__school=school).union(ParentChild.objects.filter(child__user=user, parent__school=school, child__school=school)), many=True)
                        self.response['roles']['parent_child'] = serializer.data
                elif user.is_active and Director.objects.filter(user=request.user, is_active=True, school__is_active=True, school=school).exists():
                    if Director.objects.filter(user=user, is_active=True, school__is_active=True, school=school).exists():
                        serializer = DirectorSerializer(instance=Director.objects.filter(user=user, is_active=True, school__is_active=True, school=school), many=True)
                        if 'director' not in self.response['roles']:
                            self.response['roles']['director'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['director']:
                                    self.response['roles']['director'].append(i)
                    if Teacher.objects.filter(user=user, is_active=True, school__is_active=True, school=school).exists():
                        serializer = TeacherSerializer(instance=Teacher.objects.filter(user=user, is_active=True, school__is_active=True, school=school), many=True)
                        if 'teacher' not in self.response['roles']:
                            self.response['roles']['teacher'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['teacher']:
                                    self.response['roles']['teacher'].append(i)
                    if FacultativeTeacher.objects.filter(user=user, is_active=True, school__is_active=True, school=school).exists():
                        serializer = FacultativeTeacherSerializer(instance=FacultativeTeacher.objects.filter(user=user, is_active=True, school__is_active=True, school=school), many=True)
                        if 'facultative_teacher' not in self.response['roles']:
                            self.response['roles']['facultative_teacher'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['facultative_teacher']:
                                    self.response['roles']['facultative_teacher'].append(i)
                    if Tutor.objects.filter(user=user, is_active=True, school__is_active=True, school=school).exists():
                        serializer = TutorSerializer(instance=Tutor.objects.filter(user=user, is_active=True, school__is_active=True, school=school), many=True)
                        if 'tutor' not in self.response['roles']:
                            self.response['roles']['tutor'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['tutor']:
                                    self.response['roles']['tutor'].append(i)
                    if Parent.objects.filter(user=user, is_active=True, school__is_active=True, school=school).exists():
                        serializer = ParentSerializer(instance=Parent.objects.filter(user=user, is_active=True, school__is_active=True, school=school), many=True)
                        if 'parent' not in self.response['roles']:
                            self.response['roles']['parent'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['parent']:
                                    self.response['roles']['parent'].append(i)
                    if Student.objects.filter(user=user, is_active=True, school__is_active=True, school=school).exists():
                        serializer = StudentSerializer(instance=Student.objects.filter(user=user, is_active=True, school__is_active=True, school=school), many=True)
                        if 'student' not in self.response['roles']:
                            self.response['roles']['student'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['student']:
                                    self.response['roles']['student'].append(i)
                    if Food.objects.filter(user=user, is_active=True, school__is_active=True, school=school).exists():
                        serializer = FoodSerializer(instance=Food.objects.filter(user=user, is_active=True, school__is_active=True, school=school), many=True)
                        if 'food' not in self.response['roles']:
                            self.response['roles']['food'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['food']:
                                    self.response['roles']['food'].append(i)
                    if school.is_active and ParentChild.objects.filter(parent__user=user, parent__is_active=True, parent__school=school, child__is_active=True, child__school=school).exists() or ParentChild.objects.filter(child__user=user, parent__is_active=True, parent__school=school, child__is_active=True, child__school=school).exists():
                        serializer = ParentChildSerializer(instance=ParentChild.objects.filter(parent__user=user, parent__is_active=True, parent__school=school, child__is_active=True, child__school=school).union(ParentChild.objects.filter(child__user=user, parent__is_active=True, parent__school=school, child__is_active=True, child__school=school)), many=True)
                        if 'parent_child' not in self.response['roles']:
                            self.response['roles']['parent_child'] = serializer.data
                        else:
                            for i in serializer.data:
                                if i not in self.response['roles']['parent_child']:
                                    self.response['roles']['parent_child'].append(i)
                else:
                    raise serializers.ValidationError("Permission denied")

                return Response(self.response, status=status.HTTP_200_OK)

            else:
                if request.user.is_superuser:
                    if Director.objects.filter(user=user).exists():
                        serializer = DirectorSerializer(instance=Director.objects.filter(user=user), many=True)
                        self.response['roles']['director'] = serializer.data
                    if Teacher.objects.filter(user=user).exists():
                        serializer = TeacherSerializer(instance=Teacher.objects.filter(user=user), many=True)
                        self.response['roles']['teacher'] = serializer.data
                    if FacultativeTeacher.objects.filter(user=user).exists():
                        serializer = FacultativeTeacherSerializer(instance=FacultativeTeacher.objects.filter(user=user), many=True)
                        self.response['roles']['facultative_teacher'] = serializer.data
                    if Tutor.objects.filter(user=user).exists():
                        serializer = TutorSerializer(instance=Tutor.objects.filter(user=user), many=True)
                        self.response['roles']['tutor'] = serializer.data
                    if Parent.objects.filter(user=user).exists():
                        serializer = ParentSerializer(instance=Parent.objects.filter(user=user), many=True)
                        self.response['roles']['parent'] = serializer.data
                    if Student.objects.filter(user=user).exists():
                        serializer = StudentSerializer(instance=Student.objects.filter(user=user), many=True)
                        self.response['roles']['student'] = serializer.data
                    if Food.objects.filter(user=user).exists():
                        serializer = FoodSerializer(instance=Food.objects.filter(user=user), many=True)
                        self.response['roles']['food'] = serializer.data
                    if ParentChild.objects.filter(parent__user=user).exists() or ParentChild.objects.filter(child__user=user).exists():
                        serializer = ParentChildSerializer(instance=ParentChild.objects.filter(parent__user=user).union(ParentChild.objects.filter(child__user=user)), many=True)
                        self.response['roles']['parent_child'] = serializer.data
                elif user.is_active and Director.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
                    for school in Director.objects.filter(user=request.user, is_active=True, school__is_active=True).values('school'):
                        if Director.objects.filter(user=user, is_active=True, school__id=school.get('school')).exists():
                            serializer = DirectorSerializer(instance=Director.objects.filter(user=user, is_active=True, school__id=school.get('school')), many=True)
                            if 'director' not in self.response['roles']:
                                self.response['roles']['director'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['director']:
                                        self.response['roles']['director'].append(i)
                        if Teacher.objects.filter(user=user, is_active=True, school__id=school.get('school')).exists():
                            serializer = TeacherSerializer(instance=Teacher.objects.filter(user=user, is_active=True, school__id=school.get('school')), many=True)
                            if 'teacher' not in self.response['roles']:
                                self.response['roles']['teacher'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['teacher']:
                                        self.response['roles']['teacher'].append(i)
                        if FacultativeTeacher.objects.filter(user=user, is_active=True, school__id=school.get('school')).exists():
                            serializer = FacultativeTeacherSerializer(instance=FacultativeTeacher.objects.filter(user=user, is_active=True, school__id=school.get('school')), many=True)
                            if 'facultative_teacher' not in self.response['roles']:
                                self.response['roles']['facultative_teacher'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['facultative_teacher']:
                                        self.response['roles']['facultative_teacher'].append(i)
                        if Tutor.objects.filter(user=user, is_active=True, school__id=school.get('school')).exists():
                            serializer = TutorSerializer(instance=Tutor.objects.filter(user=user, is_active=True, school__id=school.get('school')), many=True)
                            if 'tutor' not in self.response['roles']:
                                self.response['roles']['tutor'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['tutor']:
                                        self.response['roles']['tutor'].append(i)
                        if Parent.objects.filter(user=user, is_active=True, school__id=school.get('school')).exists():
                            serializer = ParentSerializer(instance=Parent.objects.filter(user=user, is_active=True, school__id=school.get('school')), many=True)
                            if 'parent' not in self.response['roles']:
                                self.response['roles']['parent'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['parent']:
                                        self.response['roles']['parent'].append(i)
                        if Student.objects.filter(user=user, is_active=True, school__id=school.get('school')).exists():
                            serializer = StudentSerializer(instance=Student.objects.filter(user=user, is_active=True, school__id=school.get('school')), many=True)
                            if 'student' not in self.response['roles']:
                                self.response['roles']['student'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['student']:
                                        self.response['roles']['student'].append(i)
                        if Food.objects.filter(user=user, is_active=True, school__id=school.get('school')).exists():
                            serializer = FoodSerializer(instance=Food.objects.filter(user=user, is_active=True, school__id=school.get('school')), many=True)
                            if 'food' not in self.response['roles']:
                                self.response['roles']['food'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['food']:
                                        self.response['roles']['food'].append(i)
                        if ParentChild.objects.filter(parent__user=user, parent__is_active=True, parent__school__id=school.get('school'), child__is_active=True, child__school__id=school.get('school')).exists() or ParentChild.objects.filter(
                                child__user=user, parent__is_active=True, parent__school__id=school.get('school'), child__is_active=True, child__school__id=school.get('school')).exists():
                            serializer = ParentChildSerializer(instance=ParentChild.objects.filter(parent__user=user, parent__is_active=True, parent__school__id=school.get('school'), child__is_active=True,
                                                                                                   child__school__id=school.get('school')).union(ParentChild.objects.filter(child__user=user, parent__is_active=True, parent__school__id=school.get('school'), child__is_active=True, child__school__id=school.get('school'))), many=True)
                            if 'parent_child' not in self.response['roles']:
                                self.response['roles']['parent_child'] = serializer.data
                            else:
                                for i in serializer.data:
                                    if i not in self.response['roles']['parent_child']:
                                        self.response['roles']['parent_child'].append(i)
                else:
                    raise serializers.ValidationError("Permission denied")

                return Response(self.response, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")


class SchoolsDBAPIView(APIView):
    """
    Получение списка школ и создание новой
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request):
        if request.user.is_superuser:
            schools = SchoolDB.objects.all()
        else:
            schools = SchoolDB.objects.filter(is_active=True)

        serializer = SchoolSerializer(instance=schools, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_superuser:
            school = request.data
            serializer = SchoolSerializer(data=school, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class SchoolDBAPIView(APIView):
    """
    Получение / редактирование / удаление школы
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            school = SchoolDB.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or school.is_active:
                serializer = SchoolSerializer(instance=school)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            school = SchoolDB.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = SchoolSerializer(instance=school, data=request.data, partial=True,
                                              context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            elif Director.objects.filter(user=request.user, is_active=True).exists() and school.is_active:
                directors = Director.objects.filter(user=request.user, is_active=True).values('school')
                for director in directors:
                    if director.get('school') == kwargs.get('pk'):
                        serializer = SchoolSerializer(instance=school, data=request.data, partial=True,
                                                      context={'request': request})
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
                raise serializers.ValidationError("Permission denied")
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def delete(self, request, *args, **kwargs):
        try:
            school = SchoolDB.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                school.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class SchoolRoles(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['surname']
    ordering_fields = '__all__'
    filterset_fields = {
        "is_active": ["exact", ],
        "role_is_active": ["exact", ],
        "date_joined": ["lte", "gte"],
        "last_login": ["lte", "gte"]
    }

    def get(self, request, model, *args, **kwargs):
        user_list = []
        try:
            school = SchoolDB.objects.get(id=kwargs.get('pk'))

            if request.user.is_superuser:

                if model.objects.filter(is_active=False, school=school).exists():
                    for role in model.objects.filter(is_active=False, school=school).values(
                            'user'):  # получаем список всех пользователей с неактивными ролями
                        user = User.objects.get(id=role.get('user'))
                        user.role_is_active = False  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if role.get('user') not in user_list:
                            user_list.append(role.get('user'))

                if model.objects.filter(is_active=True, school=school).exists():
                    for role in model.objects.filter(is_active=True, school=school).values(
                            'user'):  # получаем список всех пользователей с активными ролями
                        user = User.objects.get(id=role.get('user'))
                        user.role_is_active = True  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if role.get('user') not in user_list:
                            user_list.append(role.get('user'))

                users = User.objects.filter(id__in=user_list)
                filter_users = self.filter_queryset(users)
                page_users = self.paginate_queryset(filter_users)
                serializer = UserAdminSerializer(instance=page_users, many=True)
                return self.get_paginated_response(serializer.data)

            elif Director.objects.filter(user=request.user, is_active=True,
                                         school=school).exists() and school.is_active:

                if model.objects.filter(user__is_active=True, is_active=False, school=school).exists():
                    for role in model.objects.filter(user__is_active=True, is_active=False, school=school).values(
                            'user'):  # получаем список активных пользователей с неактивными ролями
                        user = User.objects.get(id=role.get('user'))
                        user.role_is_active = False  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if role.get('user') not in user_list:
                            user_list.append(role.get('user'))

                if model.objects.filter(user__is_active=True, is_active=True, school=school).exists():
                    for role in model.objects.filter(user__is_active=True, is_active=True, school=school).values(
                            'user'):  # получаем список активных пользователей с активными ролями
                        user = User.objects.get(id=role.get('user'))
                        user.role_is_active = True  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                        user.save()
                        if role.get('user') not in user_list:
                            user_list.append(role.get('user'))

                users = User.objects.filter(id__in=user_list)
                filter_users = self.filter_queryset(users)
                page_users = self.paginate_queryset(filter_users)
                serializer = UserSerializer(instance=page_users, many=True)
                return self.get_paginated_response(serializer.data)

            elif school.is_active:
                if school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    if model.objects.filter(user__is_active=True, is_active=True, school=school).exists():
                        for role in model.objects.filter(user__is_active=True, is_active=True, school=school).values(
                                'user'):  # получаем список с активными ролями
                            user = User.objects.get(id=role.get('user'))
                            user.role_is_active = True  # устанавливаем значение в служебное поле в БД, для фильтрации в response
                            user.save()
                            if role.get('user') not in user_list:
                                user_list.append(role.get('user'))

                    users = User.objects.filter(id__in=user_list)
                    filter_users = self.filter_queryset(users)
                    page_users = self.paginate_queryset(filter_users)
                    serializer = UserSerializer(instance=page_users, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")


class SchoolDirectorsAPIView(SchoolRoles):
    """
    Получение списка завучей школы
    """

    def get(self, request, *args, **kwargs):
        return SchoolRoles.get(self, request, *args, **kwargs, model=Director)


class SchoolTeachersAPIView(SchoolRoles):
    """
    Получение списка учителей школы
    """

    def get(self, request, *args, **kwargs):
        return SchoolRoles.get(self, request, *args, **kwargs, model=Teacher)


class SchoolFacultativeTeachersAPIView(SchoolRoles):
    """
    Получение списка учителей факультативов школы
    """

    def get(self, request, *args, **kwargs):
        return SchoolRoles.get(self, request, *args, **kwargs, model=FacultativeTeacher)


class SchoolTutorsAPIView(SchoolRoles):
    """
    Получение списка тьюторов школы
    """

    def get(self, request, *args, **kwargs):
        return SchoolRoles.get(self, request, *args, **kwargs, model=Tutor)


class SchoolParentsAPIView(SchoolRoles):
    """
    Получение списка родителей школы
    """

    def get(self, request, *args, **kwargs):
        return SchoolRoles.get(self, request, *args, **kwargs, model=Parent)


class SchoolStudentsAPIView(SchoolRoles):
    """
    Получение списка учеников школы
    """

    def get(self, request, *args, **kwargs):
        return SchoolRoles.get(self, request, *args, **kwargs, model=Student)


class SchoolFoodsAPIView(SchoolRoles):
    """
    Получение списка операторов питания школы
    """

    def get(self, request, *args, **kwargs):
        return SchoolRoles.get(self, request, *args, **kwargs, model=Food)


class SchoolParentChildAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['surname']
    ordering_fields = '__all__'
    filterset_fields = {
        # "is_active": ["exact", ],
        # "role_is_active": ["exact", ],
        # "date_joined": ["lte", "gte"],
        # "last_login": ["lte", "gte"]
    }

    def get(self, request, *args, **kwargs):
        user_list = []
        try:
            school = SchoolDB.objects.get(id=kwargs.get('pk'))

            if request.user.is_superuser:
                if ParentChild.objects.filter(parent__school=school, child__school=school).exists():
                    user_list = ParentChild.objects.filter(parent__school=school, child__school=school)
                filter_users = self.filter_queryset(user_list)
                page_users = self.paginate_queryset(filter_users)
                serializer = ParentChildSerializer(instance=page_users, many=True)
                return self.get_paginated_response(serializer.data)

            elif Director.objects.filter(user=request.user, is_active=True, school=school).exists() and school.is_active:
                if ParentChild.objects.filter(parent__user__is_active=True, child__user__is_active=True, parent__school=school, child__school=school).exists():
                    user_list = ParentChild.objects.filter(parent__user__is_active=True, child__user__is_active=True, parent__school=school, child__school=school)
                filter_users = self.filter_queryset(user_list)
                page_users = self.paginate_queryset(filter_users)
                serializer = ParentChildSerializer(instance=page_users, many=True)
                return self.get_paginated_response(serializer.data)

            elif school.is_active:
                if school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    if ParentChild.objects.filter(parent__user__is_active=True, child__user__is_active=True, parent__is_active=True, child__is_active=True, parent__school=school, child__school=school).exists():
                        user_list = ParentChild.objects.filter(parent__user__is_active=True, child__user__is_active=True, parent__is_active=True, child__is_active=True, parent__school=school, child__school=school)
                    filter_users = self.filter_queryset(user_list)
                    page_users = self.paginate_queryset(filter_users)
                    serializer = ParentChildSerializer(instance=page_users, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")
