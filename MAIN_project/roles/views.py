import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.utils import timezone

from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
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

from .serializers import DirectorSerializer
from main_app.models import Photo, User, SchoolDB  #, Object, Cabinet, Class, Group, Lesson, TimeLesson, Schedule
from main_app.serializers import UserSerializer, UserAdminSerializer
from main_app.views import IsActive, get_user_schools, CustomJWTAuthentication
from .models import Director, Teacher, FacultativeTeacher, Tutor, Parent, Student, Food, ParentChild
from .serializers import DirectorSerializer, TeacherSerializer, FacultativeTeacherSerializer, TutorSerializer, ParentSerializer, StudentSerializer, FoodSerializer, ParentChildSerializer

import os


class Roles(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    ordering_fields = '__all__'
    filterset_fields = {
        "is_active": ["exact", ],
    }

    def get(self, request, model, model_serializer, *args, **kwargs):
        if request.user.is_superuser:
            models = model.objects.all()
            filter_users = self.filter_queryset(models)
            page_users = self.paginate_queryset(filter_users)
            serializer = model_serializer(instance=page_users, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            raise serializers.ValidationError("Permission denied")

    def post(self, request, model_serializer):
        data = request.data

        if request.user.is_superuser:
            serializer = model_serializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif Director.objects.filter(user=request.user, is_active=True, school__id=data['school_id']).exists():
            if User.objects.filter(id=data['user_id']).exists() and User.objects.get(id=data['user_id']).is_active and SchoolDB.objects.get(id=data['school_id']).is_active:
                serializer = model_serializer(data=data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError("Permission denied")

        else:
            raise serializers.ValidationError("Permission denied")


class Role(APIView):
    """
    Получение / редактирование / удаление роли
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, model, model_serializer, *args, **kwargs):
        try:
            role = model.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = model_serializer(instance=role)
            elif Director.objects.filter(user=request.user, is_active=True, school=role.school, school__is_active=True).exists() and role.user.is_active:
                serializer = model_serializer(instance=role)
            elif role.is_active and role.user.is_active and role.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = model_serializer(instance=role)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, model, model_serializer, *args, **kwargs):
        try:
            role = model.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = model_serializer(instance=role, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            elif Director.objects.filter(user=request.user, is_active=True, school=role.school, school__is_active=True).exists() and role.user.is_active:
                serializer = model_serializer(instance=role, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def delete(self, request, model, *args, **kwargs):
        try:
            role = model.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                role.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif Director.objects.filter(user=request.user, is_active=True, school=role.school, school__is_active=True).exists() and role.user.is_active:
                role.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class DirectorsAPIView(Roles):

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=Director, model_serializer=DirectorSerializer, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Roles.post(self, request, model_serializer=DirectorSerializer)


class DirectorAPIView(Role):

    def get(self, request, *args, **kwargs):
        return Role.get(self, request, model=Director, model_serializer=DirectorSerializer, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Role.patch(self, request, model=Director, model_serializer=DirectorSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return Role.delete(self, request, model=Director, *args, **kwargs)


class TeachersAPIView(Roles):

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=Teacher, model_serializer=TeacherSerializer, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Roles.post(self, request, model_serializer=TeacherSerializer)


class TeacherAPIView(Role):

    def get(self, request, *args, **kwargs):
        return Role.get(self, request, model=Teacher, model_serializer=TeacherSerializer, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Role.patch(self, request, model=Teacher, model_serializer=TeacherSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return Role.delete(self, request, model=Teacher, *args, **kwargs)


class FacultativeTeachersAPIView(Roles):

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=FacultativeTeacher, model_serializer=FacultativeTeacherSerializer, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Roles.post(self, request, model_serializer=FacultativeTeacherSerializer)


class FacultativeTeacherAPIView(Role):

    def get(self, request, *args, **kwargs):
        return Role.get(self, request, model=FacultativeTeacher, model_serializer=FacultativeTeacherSerializer, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Role.patch(self, request, model=FacultativeTeacher, model_serializer=FacultativeTeacherSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return Role.delete(self, request, model=FacultativeTeacher, *args, **kwargs)


class TutorsAPIView(Roles):

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=Tutor, model_serializer=TutorSerializer, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Roles.post(self, request, model_serializer=TutorSerializer)


class TutorAPIView(Role):

    def get(self, request, *args, **kwargs):
        return Role.get(self, request, model=Tutor, model_serializer=TutorSerializer, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Role.patch(self, request, model=Tutor, model_serializer=TutorSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return Role.delete(self, request, model=Tutor, *args, **kwargs)


class ParentsAPIView(Roles):

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=Parent, model_serializer=ParentSerializer, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Roles.post(self, request, model_serializer=ParentSerializer)


class ParentAPIView(Role):

    def get(self, request, *args, **kwargs):
        return Role.get(self, request, model=Parent, model_serializer=ParentSerializer, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Role.patch(self, request, model=Parent, model_serializer=ParentSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return Role.delete(self, request, model=Parent, *args, **kwargs)


class StudentsAPIView(Roles):

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=Student, model_serializer=StudentSerializer, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Roles.post(self, request, model_serializer=StudentSerializer)


class StudentAPIView(Role):

    def get(self, request, *args, **kwargs):
        return Role.get(self, request, model=Student, model_serializer=StudentSerializer, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Role.patch(self, request, model=Student, model_serializer=StudentSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return Role.delete(self, request, model=Student, *args, **kwargs)


class FoodsAPIView(Roles):

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=Food, model_serializer=FoodSerializer, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Roles.post(self, request, model_serializer=FoodSerializer)


class FoodAPIView(Role):

    def get(self, request, *args, **kwargs):
        return Role.get(self, request, model=Food, model_serializer=FoodSerializer, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Role.patch(self, request, model=Food, model_serializer=FoodSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return Role.delete(self, request, model=Food, *args, **kwargs)


class ParentChildsAPIView(Roles):
    """
    Получение / создание / редактирование / удаление связей родитель-дети
    """
    filterset_fields = {}

    def get(self, request, *args, **kwargs):
        return Roles.get(self, request, model=ParentChild, model_serializer=ParentChildSerializer, *args, **kwargs)

    def post(self, request, **kwargs):
        """переопределяем метод post наследуемого класса, т.к. он не подходит
        """
        data = request.data

        if request.user.is_superuser:
            serializer = ParentChildSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif Director.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            try:
                parent = Parent.objects.get(id=data['parent_id'])
                child = Student.objects.get(id=data['child_id'])
                if not parent.user.is_active or not child.user.is_active:
                    raise serializers.ValidationError("Permission denied")
                if not Director.objects.filter(user=request.user, is_active=True, school=parent.school, school__is_active=True).exists() or not Director.objects.filter(user=request.user, is_active=True, school=child.school, school__is_active=True).exists():
                    raise serializers.ValidationError("Permission denied")
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong ID")
            serializer = ParentChildSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class ParentChildAPIView(APIView):
    """
    Получение / редактирование / удаление школы
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            role = ParentChild.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = ParentChildSerializer(instance=role)
            elif Director.objects.filter(user=request.user, is_active=True, school=role.parent.school, school__is_active=True).exists() and role.child.user.is_active and role.parent.user.is_active:
                serializer = ParentChildSerializer(instance=role)
            elif role.child.is_active and role.parent.is_active and role.child.user.is_active and role.parent.user.is_active and role.parent.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = ParentChildSerializer(instance=role)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            role = ParentChild.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = ParentChildSerializer(instance=role, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            elif Director.objects.filter(user=request.user, is_active=True, school=role.parent.school, school__is_active=True).exists() and role.child.user.is_active and role.parent.user.is_active:
                serializer = ParentChildSerializer(instance=role, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def delete(self, request, *args, **kwargs):
        try:
            role = ParentChild.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                role.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif Director.objects.filter(user=request.user, is_active=True, school=role.parent.school, school__is_active=True).exists() and role.child.user.is_active and role.parent.user.is_active:
                role.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")
