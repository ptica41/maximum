from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import FileResponse
from django.utils import timezone

from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from random import randint


from .models import Object, Cabinet, Class, Group, Lesson, TimeLesson, Schedule, StudentClass, StudentGroup
from .serializers import ObjectSerializer, CabinetSerializer, ClassSerializer, GroupSerializer, LessonSerializer, TimeLessonSerializer, ScheduleSerializer, StudentClassSerializer, StudentGroupSerializer

from main_app.models import Photo, User, SchoolDB
from main_app.serializers import UserSerializer, UserAdminSerializer
from main_app.views import IsActive, get_user_schools, CustomJWTAuthentication

from roles.models import Director, Teacher, FacultativeTeacher, Student


class ObjectsAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['name']
    ordering_fields = '__all__'
    filterset_fields = {
        "school_id": ["exact", ]
    }

    def get(self, request):
        if request.user.is_superuser:
            objects = Object.objects.all()
            filter_objects = self.filter_queryset(objects)
            page_objects = self.paginate_queryset(filter_objects)
            serializer = ObjectSerializer(instance=page_objects, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            if 'school_id' in request.query_params:
                if int(request.query_params.get('school_id')) in [i.get('school') for i in get_user_schools(request.user)]:
                    objects = Object.objects.filter(school_id=request.query_params.get('school_id'))
                    filter_objects = self.filter_queryset(objects)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ObjectSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif not SchoolDB.objects.filter(id=int(request.query_params.get('school_id'))).exists():
                    raise serializers.ValidationError("Wrong school ID")
                else:
                    raise serializers.ValidationError("Permission denied")

            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                objects = Object.objects.filter(school_id__in=schools)
                filter_objects = self.filter_queryset(objects)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = ObjectSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school__id=data.get('school_id'), school__is_active=True).exists():
            serializer = ObjectSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class ObjectAPIView(APIView):
    """
    Получение / редактирование / удаление предмета
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            obj = Object.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or obj.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = ObjectSerializer(instance=obj)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            obj = Object.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=obj.school, school__is_active=True).exists():
                serializer = ObjectSerializer(instance=obj, data=request.data, partial=True, context={'request': request})
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
            obj = Object.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=obj.school, school__is_active=True).exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class CabinetsAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['name']
    ordering_fields = '__all__'
    filterset_fields = {
        "school_id": ["exact", ]
    }

    def get(self, request):
        if request.user.is_superuser:
            cabinets = Cabinet.objects.all()
            filter_objects = self.filter_queryset(cabinets)
            page_objects = self.paginate_queryset(filter_objects)
            serializer = CabinetSerializer(instance=page_objects, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            if 'school_id' in request.query_params:
                if int(request.query_params.get('school_id')) in [i.get('school') for i in get_user_schools(request.user)]:
                    cabinets = Cabinet.objects.filter(school_id=request.query_params.get('school_id'))
                    filter_objects = self.filter_queryset(cabinets)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = CabinetSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif not SchoolDB.objects.filter(id=int(request.query_params.get('school_id'))).exists():
                    raise serializers.ValidationError("Wrong school ID")
                else:
                    raise serializers.ValidationError("Permission denied")

            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                cabinets = Cabinet.objects.filter(school_id__in=schools)
                filter_objects = self.filter_queryset(cabinets)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = CabinetSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school__id=data.get('school_id'), school__is_active=True).exists():
            serializer = CabinetSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class CabinetAPIView(APIView):
    """
    Получение / редактирование / удаление кабинета
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            cabinet = Cabinet.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or cabinet.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = CabinetSerializer(instance=cabinet)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            cabinet = Cabinet.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=cabinet.school, school__is_active=True).exists():
                serializer = CabinetSerializer(instance=cabinet, data=request.data, partial=True, context={'request': request})
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
            cabinet = Cabinet.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=cabinet.school, school__is_active=True).exists():
                cabinet.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class ClassesAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['name']
    ordering_fields = '__all__'

    def get(self, request):
        if 'HTTP_SCHOOL' in request.META.keys():  # TODO: переделать все с header на query
            try:
                school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])
                if request.user.is_superuser:
                    classes = Class.objects.filter(cabinet__school=school)
                    filter_objects = self.filter_queryset(classes)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ClassSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    classes = Class.objects.filter(cabinet__school=school)
                    filter_objects = self.filter_queryset(classes)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ClassSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")
        else:
            if request.user.is_superuser:
                classes = Class.objects.all()
                filter_objects = self.filter_queryset(classes)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = ClassSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                cabinets = Class.objects.filter(cabinet__school_id__in=schools)
                filter_objects = self.filter_queryset(cabinets)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = ClassSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        try:
            if data.get('cabinet_id'):
                school = Cabinet.objects.get(id=data.get('cabinet_id')).school
            else:
                raise serializers.ValidationError([{"title": "emptyCabinetID", "description": "поле cabinet_id обязательное"}])
        except ObjectDoesNotExist:
            raise serializers.ValidationError([{"title": "cabinetIsNotExist", "description": "кабинета с таким id не существует"}])
        if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
            serializer = ClassSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class ClassAPIView(APIView):
    """
    Получение / редактирование / удаление класса
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            cls = Class.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or cls.cabinet.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = ClassSerializer(instance=cls)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            cls = Class.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=cls.cabinet.school, school__is_active=True).exists():
                serializer = ClassSerializer(instance=cls, data=request.data, partial=True, context={'request': request})
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
            cls = Class.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=cls.cabinet.school, school__is_active=True).exists():
                cls.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class GroupsAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['name']
    ordering_fields = '__all__'

    def get(self, request):
        if 'HTTP_SCHOOL' in request.META.keys():
            try:
                school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])
                if request.user.is_superuser:
                    groups = Group.objects.filter(Q(school=school) | Q(cls__cabinet__school=school))
                    filter_objects = self.filter_queryset(groups)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = GroupSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    groups = Group.objects.filter(Q(school=school) | Q(cls__cabinet__school=school))
                    filter_objects = self.filter_queryset(groups)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = GroupSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")
        else:
            if request.user.is_superuser:
                groups = Group.objects.all()
                filter_objects = self.filter_queryset(groups)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = GroupSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                groups = Group.objects.filter(Q(school_id__in=schools) | Q(cls__cabinet__school_id__in=schools))
                filter_objects = self.filter_queryset(groups)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = GroupSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        try:
            if data.get('cls_id'):
                school = Class.objects.get(id=data.get('cls_id')).cabinet.school
            elif data.get('school_id'):
                school = SchoolDB.objects.get(id=data.get('school_id'))
            else:
                raise serializers.ValidationError([{"title": "nullID", "description": "необходимо указать либо ID школы, либо ID класса"}])
        except ObjectDoesNotExist:
            raise serializers.ValidationError([{"title": "schoolOrClassIsNotExist", "description": "школы или класса с таким id не существует"}])
        if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
            serializer = GroupSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class GroupAPIView(APIView):
    """
    Получение / редактирование / удаление группы
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id=kwargs.get('pk'))
            school = (group.school if group.school else group.cls.cabinet.school)
            if request.user.is_superuser or school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = GroupSerializer(instance=group)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id=kwargs.get('pk'))
            school = (group.school if group.school else group.cls.cabinet.school)
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
                serializer = GroupSerializer(instance=group, data=request.data, partial=True, context={'request': request})
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
            group = Group.objects.get(id=kwargs.get('pk'))
            school = (group.school if group.school else group.cls.cabinet.school)
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
                group.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class LessonsAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    ordering_fields = '__all__'

    def get(self, request):
        if 'HTTP_SCHOOL' in request.META.keys():
            try:
                school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])
                if request.user.is_superuser:
                    lessons = Lesson.objects.filter(object__school_id=school)
                    filter_objects = self.filter_queryset(lessons)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = LessonSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    lessons = Lesson.objects.filter(object__school_id=school)
                    filter_objects = self.filter_queryset(lessons)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = LessonSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")
        else:
            if request.user.is_superuser:
                lessons = Lesson.objects.all()
                filter_objects = self.filter_queryset(lessons)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = LessonSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                lessons = Lesson.objects.filter(object__school_id__in=schools)
                filter_objects = self.filter_queryset(lessons)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = LessonSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        try:
            school = Object.objects.get(id=data.get('object_id')).school
        except ObjectDoesNotExist:
            raise serializers.ValidationError([{"title": "objectIsNotExist", "description": "Поле object_id обязательное | предмета с таким id не существует"}])
        if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
            serializer = LessonSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class LessonAPIView(APIView):
    """
    Получение / редактирование / удаление урока
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=kwargs.get('pk'))
            school = lesson.object.school
            if request.user.is_superuser or school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = LessonSerializer(instance=lesson)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=kwargs.get('pk'))
            school = lesson.object.school
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
                serializer = LessonSerializer(instance=lesson, data=request.data, partial=True, context={'request': request})
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
            lesson = Lesson.objects.get(id=kwargs.get('pk'))
            school = lesson.object.school
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
                lesson.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class TimeLessonsAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    search_fields = ['period']
    ordering_fields = '__all__'
    filterset_fields = {
        "school_id": ["exact", ]
    }

    def get(self, request):
        if request.user.is_superuser:
            time_lessons = TimeLesson.objects.all()
            filter_objects = self.filter_queryset(time_lessons)
            page_objects = self.paginate_queryset(filter_objects)
            serializer = TimeLessonSerializer(instance=page_objects, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            if 'school_id' in request.query_params:
                if int(request.query_params.get('school_id')) in [i.get('school') for i in get_user_schools(request.user)]:
                    time_lessons = TimeLesson.objects.filter(school_id=request.query_params.get('school_id'))
                    filter_objects = self.filter_queryset(time_lessons)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = TimeLessonSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif not SchoolDB.objects.filter(id=int(request.query_params.get('school_id'))).exists():
                    raise serializers.ValidationError("Wrong school ID")
                else:
                    raise serializers.ValidationError("Permission denied")

            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                time_lessons = TimeLesson.objects.filter(school_id__in=schools)
                filter_objects = self.filter_queryset(time_lessons)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = TimeLessonSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school__id=data.get('school_id'), school__is_active=True).exists():
            serializer = TimeLessonSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class TimeLessonAPIView(APIView):
    """
    Получение / редактирование / удаление времени расписания уроков
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            obj = TimeLesson.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or obj.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = TimeLessonSerializer(instance=obj)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            obj = TimeLesson.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=obj.school, school__is_active=True).exists():
                serializer = TimeLessonSerializer(instance=obj, data=request.data, partial=True, context={'request': request})
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
            obj = TimeLesson.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=obj.school, school__is_active=True).exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class SchedulesAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    # search_fields = ['name']
    filterset_fields = {
        "start": ["gte"],
        "end": ["lte"],
        "number": ["exact"],
        "is_cancelled": ["exact"],
        "student_id": ["exact"],
        "group_id": ["exact"],
        "cls_id": ["exact"],
        "cabinet_id": ["exact"]
    }
    ordering_fields = '__all__'

    def get(self, request):
        school = 0
        if 'school_id' in request.query_params:
            try:
                school = SchoolDB.objects.get(id=request.query_params.get('school_id'))
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")

        if 'teacher_id' in request.query_params:
            try:
                teacher = Teacher.objects.get(id=request.query_params.get('teacher_id'))
                if request.user.is_superuser:
                    if school:
                        schedules = Schedule.objects.filter(lesson__teacher=teacher, lesson__object__school=school)
                    else:
                        schedules = Schedule.objects.filter(lesson__teacher=teacher)
                    filter_objects = self.filter_queryset(schedules)
                    if 'facultative_teacher_id' in request.query_params:
                        try:
                            facultative_teacher = FacultativeTeacher.objects.get(
                                id=request.query_params.get('facultative_teacher_id'))
                            if request.user.is_superuser:
                                if school:
                                    schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher, lesson__object__school=school)
                                else:
                                    schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher)
                                filter_objects = filter_objects.union(self.filter_queryset(schedules))
                        except ObjectDoesNotExist:
                            raise serializers.ValidationError("Wrong facultative teacher ID")

                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ScheduleSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif teacher.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    if school:
                        schedules = Schedule.objects.filter(lesson__teacher=teacher, lesson__object__school=school)
                    else:
                        schedules = Schedule.objects.filter(lesson__teacher=teacher)
                    filter_objects = self.filter_queryset(schedules)
                    if 'facultative_teacher_id' in request.query_params:
                        try:
                            facultative_teacher = FacultativeTeacher.objects.get(id=request.query_params.get('facultative_teacher_id'))
                            if facultative_teacher.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                                if school:
                                    schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher, lesson__object__school=school)
                                else:
                                    schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher)
                                filter_objects = filter_objects.union(self.filter_queryset(schedules))
                            else:
                                raise serializers.ValidationError("Permission denied")
                        except ObjectDoesNotExist:
                            raise serializers.ValidationError("Wrong facultative teacher ID")

                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ScheduleSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong teacher ID")
        elif 'facultative_teacher_id' in request.query_params:
            try:
                facultative_teacher = FacultativeTeacher.objects.get(id=request.query_params.get('facultative_teacher_id'))
                if request.user.is_superuser:
                    if school:
                        schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher, lesson__object__school=school)
                    else:
                        schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher)
                    filter_objects = self.filter_queryset(schedules)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ScheduleSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif facultative_teacher.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    if school:
                        schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher, lesson__object__school=school)
                    else:
                        schedules = Schedule.objects.filter(lesson__facultative_teacher=facultative_teacher)
                    filter_objects = self.filter_queryset(schedules)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ScheduleSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong facultative teacher ID")
        elif 'studentAll_id' in request.query_params:
            try:
                groups = []
                clss = []
                student = Student.objects.get(id=request.query_params.get('studentAll_id'))
                if request.user.is_superuser or student.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    for group in StudentGroup.objects.filter(student=student):
                        groups.append(group.group.id)
                    for cls in StudentClass.objects.filter(student=student):
                        clss.append(cls.cls.id)
                    schedules = Schedule.objects.filter(student=student)
                    schedules_cls = Schedule.objects.filter(cls__id__in=clss)
                    schedules_groups = Schedule.objects.filter(group__id__in=groups)
                    filter_objects = self.filter_queryset(schedules).union(schedules_cls).union(schedules_groups)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = ScheduleSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong student ID")
        else:
            if request.user.is_superuser:
                if school:
                    schedules = Schedule.objects.filter(lesson__object__school=school)
                else:
                    schedules = Schedule.objects.all()
                filter_objects = self.filter_queryset(schedules)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = ScheduleSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                if school:
                    schedules = Schedule.objects.filter(lesson__object__school=school)
                else:
                    schedules = Schedule.objects.filter(lesson__object__school__in=schools)
                filter_objects = self.filter_queryset(schedules)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = ScheduleSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        if data.get('lesson_id'):
            try:
                school = Lesson.objects.get(id=data.get('lesson_id')).object.school
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong lesson ID")
        else:
            raise serializers.ValidationError([{"title": "nullID", "description": "необходимо указать ID урока"}])

        if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=school, school__is_active=True).exists():
            serializer = ScheduleSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError("Permission denied")


class ScheduleAPIView(APIView):
    """
    Получение / редактирование / удаление расписания уроков
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            schedule = Schedule.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or schedule.lesson.object.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = ScheduleSerializer(instance=schedule)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            schedule = Schedule.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=schedule.lesson.object.school, school__is_active=True).exists():
                serializer = ScheduleSerializer(instance=schedule, data=request.data, partial=True, context={'request': request})
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
            schedule = Schedule.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser or Director.objects.filter(user=request.user, is_active=True, school=schedule.lesson.object.school, school__is_active=True).exists():
                schedule.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class StudentClassesAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    filterset_fields = {
        "cls_id": ["exact"],
        "student_id": ["exact"],
    }
    ordering_fields = '__all__'

    def get(self, request):
        if 'HTTP_SCHOOL' in request.META.keys():  # TODO: переделать все с header на query
            try:
                school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])
                if request.user.is_superuser:
                    student_classes = StudentClass.objects.filter(cls__cabinet__school=school)
                    filter_objects = self.filter_queryset(student_classes)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = StudentClassSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif Director.objects.filter(is_active=True, user=request.user, school=school).exists():
                    student_classes = StudentClass.objects.filter(student__user__is_active=True, cls__cabinet__school=school)
                    filter_objects = self.filter_queryset(student_classes)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = StudentClassSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    student_classes = StudentClass.objects.filter(student__is_active=True, student__user__is_active=True, cls__cabinet__school=school)
                    filter_objects = self.filter_queryset(student_classes)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = StudentClassSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")
        else:
            if request.user.is_superuser:
                student_classes = StudentClass.objects.all()
                filter_objects = self.filter_queryset(student_classes)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = StudentClassSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            elif Director.objects.filter(is_active=True, user=request.user).exists():
                schools = [i.get('school') for i in get_user_schools(request.user)]  # TODO: исправить - при таком подходе мы также можем получить связи с неактивными ролями "ученик" в школах, где юзер не является завучем (с другой ролью)
                student_classes = StudentClass.objects.filter(student__user__is_active=True, cls__cabinet__school_id__in=schools)
                filter_objects = self.filter_queryset(student_classes)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = StudentClassSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                student_classes = StudentClass.objects.filter(student__is_active=True, student__user__is_active=True, cls__cabinet__school_id__in=schools)
                filter_objects = self.filter_queryset(student_classes)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = StudentClassSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        if request.user.is_superuser:
            serializer = StudentClassSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif Director.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            serializer = StudentClassSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            raise serializers.ValidationError("Permission denied")


class StudentClassAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            student_classes = StudentClass.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = StudentClassSerializer(instance=student_classes)
            elif Director.objects.filter(user=request.user, is_active=True, school=student_classes.student.school, school__is_active=True).exists():
                serializer = StudentClassSerializer(instance=student_classes)
            elif student_classes.cls.cabinet.school.is_active and student_classes.student.is_active and student_classes.student.user.is_active and student_classes.cls.cabinet.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = StudentClassSerializer(instance=student_classes)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            student_classes = StudentClass.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = StudentClassSerializer(instance=student_classes, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            elif Director.objects.filter(user=request.user, is_active=True, school__is_active=True, school=student_classes.student.school).exists():
                serializer = StudentClassSerializer(instance=student_classes, data=request.data, partial=True, context={'request': request})
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
            student_classes = StudentClass.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                student_classes.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif Director.objects.filter(user=request.user, is_active=True, school__is_active=True, school=student_classes.student.school).exists():
                student_classes.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")


class StudentGroupsAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    filterset_fields = {
        "group_id": ["exact"],
        "student_id": ["exact"],
    }
    ordering_fields = '__all__'

    def get(self, request):
        if 'HTTP_SCHOOL' in request.META.keys():  # TODO: переделать все с header на query
            try:
                school = SchoolDB.objects.get(id=request.META['HTTP_SCHOOL'])
                if request.user.is_superuser:
                    student_groups = StudentGroup.objects.filter(student__school=school)
                    filter_objects = self.filter_queryset(student_groups)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = StudentGroupSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif Director.objects.filter(is_active=True, user=request.user, school=school).exists():
                    student_groups = StudentGroup.objects.filter(student__user__is_active=True, student__school=school)
                    filter_objects = self.filter_queryset(student_groups)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = StudentGroupSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                elif school.id in [i.get('school') for i in get_user_schools(request.user)]:
                    student_groups = StudentGroup.objects.filter(student__is_active=True, student__user__is_active=True, student__school=school)
                    filter_objects = self.filter_queryset(student_groups)
                    page_objects = self.paginate_queryset(filter_objects)
                    serializer = StudentGroupSerializer(instance=page_objects, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    raise serializers.ValidationError("Permission denied")

            except ObjectDoesNotExist:
                raise serializers.ValidationError("Wrong school ID")
        else:
            if request.user.is_superuser:
                student_groups = StudentGroup.objects.all()
                filter_objects = self.filter_queryset(student_groups)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = StudentGroupSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            elif Director.objects.filter(is_active=True, user=request.user).exists():
                schools = [i.get('school') for i in get_user_schools(request.user)] # TODO: исправить - при таком подходе мы также можем получить связи с неактивными ролями "ученик" в школах, где юзер не является завучем (с другой ролью)
                student_groups = StudentGroup.objects.filter(student__user__is_active=True, student__school_id__in=schools)
                filter_objects = self.filter_queryset(student_groups)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = StudentGroupSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                schools = [i.get('school') for i in get_user_schools(request.user)]
                student_groups = StudentGroup.objects.filter(student__is_active=True, student__user__is_active=True, student__school_id__in=schools)
                filter_objects = self.filter_queryset(student_groups)
                page_objects = self.paginate_queryset(filter_objects)
                serializer = StudentGroupSerializer(instance=page_objects, many=True)
                return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        if request.user.is_superuser:
            serializer = StudentGroupSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif Director.objects.filter(user=request.user, is_active=True, school__is_active=True).exists():
            serializer = StudentGroupSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            raise serializers.ValidationError("Permission denied")


class StudentGroupAPIView(GenericAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request, *args, **kwargs):
        try:
            student_groups = StudentGroup.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = StudentGroupSerializer(instance=student_groups)
            elif Director.objects.filter(user=request.user, is_active=True, school=student_groups.student.school, school__is_active=True).exists():
                serializer = StudentGroupSerializer(instance=student_groups)
            elif student_groups.student.school.is_active and student_groups.student.is_active and student_groups.student.user.is_active and student_groups.student.school.id in [i.get('school') for i in get_user_schools(request.user)]:
                serializer = StudentGroupSerializer(instance=student_groups)
            else:
                raise serializers.ValidationError("Permission denied")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Wrong ID")

    def patch(self, request, *args, **kwargs):
        try:
            student_groups = StudentGroup.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                serializer = StudentGroupSerializer(instance=student_groups, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            elif Director.objects.filter(user=request.user, is_active=True, school__is_active=True, school=student_groups.student.school).exists():
                serializer = StudentGroupSerializer(instance=student_groups, data=request.data, partial=True, context={'request': request})
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
            student_groups = StudentGroup.objects.get(id=kwargs.get('pk'))
            if request.user.is_superuser:
                student_groups.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif Director.objects.filter(user=request.user, is_active=True, school__is_active=True, school=student_groups.student.school).exists():
                student_groups.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise serializers.ValidationError("Permission denied")

        except ObjectDoesNotExist:
            raise serializers.ValidationError("wrong ID")
