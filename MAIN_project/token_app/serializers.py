from django.contrib.auth import authenticate

from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError

from main_app.models import Photo, User, SchoolDB
from main_app.serializers import UserAdminSerializer, UserSerializer, SchoolSerializer, PhotoSerializer
from roles.models import Director, Teacher, FacultativeTeacher, Tutor, Parent, Student, Food, ParentChild
from roles.serializers import ParentChildSerializer, DirectorSerializer, TeacherSerializer, FacultativeTeacherSerializer, TutorSerializer, ParentSerializer, StudentSerializer, FoodSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределяем сериализатор для создания пары токенов
    В response добавляем срок действия access токена в unix-формате, данные профиля, роли и школы пользователя
    """
    data = {}

    def validate(self, attrs):

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password']
        }

        if not User.objects.filter(username=authenticate_kwargs['username']).exists():
            raise AuthenticationFailed([{"title": "invalidUsername", "description": "Неверный юзернейм"}])

        if not User.objects.get(username=authenticate_kwargs['username']).is_active:
            raise AuthenticationFailed([{"title": "inactiveUser", "description": "Неактивный пользователь"}])

        user = authenticate(request=self.context['request'], **authenticate_kwargs)

        if user is None:
            raise AuthenticationFailed([{"title": "invalidPassword", "description": "Неверный пароль"}])

        token_data = super().validate(attrs)
        self.data['roles'] = {}
        self.data['schools'] = []
        self.data['children'] = []
        token_data['exp'] = AccessToken(token_data['access']).payload['exp']
        self.data['token_data'] = token_data

        serializer = UserSerializer(instance=self.user)
        self.data['user'] = serializer.data

        if Director.objects.filter(user=self.user, is_active=True, school__is_active=True).exists():
            zav = Director.objects.filter(user=self.user, is_active=True, school__is_active=True)
            serializer = DirectorSerializer(instance=zav, many=True)
            self.data['roles']['director'] = serializer.data
            for i in zav:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.data['schools']:
                    self.data['schools'].append(serializer.data)

        if Teacher.objects.filter(user=self.user, is_active=True, school__is_active=True).exists():
            teacher = Teacher.objects.filter(user=self.user, is_active=True, school__is_active=True)
            serializer = TeacherSerializer(instance=teacher, many=True)
            self.data['roles']['teacher'] = serializer.data
            for i in teacher:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.data['schools']:
                    self.data['schools'].append(serializer.data)

        if FacultativeTeacher.objects.filter(user=self.user, is_active=True, school__is_active=True).exists():
            facultative_teacher = FacultativeTeacher.objects.filter(user=self.user, is_active=True, school__is_active=True)
            serializer = FacultativeTeacherSerializer(instance=facultative_teacher, many=True)
            self.data['roles']['facultative_teacher'] = serializer.data
            for i in facultative_teacher:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.data['schools']:
                    self.data['schools'].append(serializer.data)

        if Tutor.objects.filter(user=self.user, is_active=True, school__is_active=True).exists():
            tutor = Tutor.objects.filter(user=self.user, is_active=True, school__is_active=True)
            serializer = TutorSerializer(instance=tutor, many=True)
            self.data['roles']['tutor'] = serializer.data
            for i in tutor:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.data['schools']:
                    self.data['schools'].append(serializer.data)

        if Parent.objects.filter(user=self.user, is_active=True, school__is_active=True).exists():
            parent = Parent.objects.filter(user=self.user, is_active=True, school__is_active=True)
            serializer = ParentSerializer(instance=parent, many=True)
            self.data['roles']['parent'] = serializer.data
            for i in parent:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.data['schools']:
                    self.data['schools'].append(serializer.data)

        if Student.objects.filter(user=self.user, is_active=True, school__is_active=True).exists():
            student = Student.objects.filter(user=self.user, is_active=True, school__is_active=True)
            serializer = StudentSerializer(instance=student, many=True)
            self.data['roles']['student'] = serializer.data
            for i in student:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.data['schools']:
                    self.data['schools'].append(serializer.data)

        if Food.objects.filter(user=self.user, is_active=True, school__is_active=True).exists():
            food = Food.objects.filter(user=self.user, is_active=True, school__is_active=True)
            serializer = FoodSerializer(instance=food, many=True)
            self.data['roles']['food'] = serializer.data
            for i in food:
                serializer = SchoolSerializer(instance=i.school)
                if serializer.data not in self.data['schools']:
                    self.data['schools'].append(serializer.data)

        if SchoolDB.objects.filter(is_active=True).exists():
            for school in SchoolDB.objects.filter(is_active=True):
                if Parent.objects.filter(user=self.user, school=school).exists():
                    for parent in Parent.objects.filter(user=self.user, school=school):
                        for child in ParentChild.objects.filter(parent=parent, child__user__is_active=True):
                            serializer = UserSerializer(instance=child.child.user)
                            self.data['children'].append(serializer.data)

        return self.data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Переопределяем сериализатор для обновления пары токенов
    В response добавляем срок действия access токена в unix-формате
    """

    def validate(self, attrs):
        refresh = attrs.get('refresh')

        if refresh:
            if BlacklistedToken.objects.filter(token_id__token=refresh).exists():
                raise ParseError([{"title": "refreshInBlacklist", "description": "refresh токен в черном списке (срок действия истек/использован ранее)"}])
        else:
            raise ParseError([{"title": "refreshIsNull", "description": "Отсутствует refresh токен"}])
        try:
            data = super().validate(attrs)
        except TokenError as e:
            raise ParseError([{"title": "invalidRefresh", "description": "недействительный refresh токен"}])

        token_info = AccessToken(data['access']).payload
        data['exp'] = token_info['exp']
        return data
