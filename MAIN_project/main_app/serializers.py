from os import urandom

from django.conf import settings

from rest_framework import serializers

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from roles.models import Director, Teacher, FacultativeTeacher, Tutor, Parent, Student, Food, ParentChild
from .models import Photo, User, SchoolDB  #, Object, Cabinet, Class, Group, Lesson, TimeLesson, Schedule


def encrypt_pswrd(password):
    """
    Функция шифрования с помощью симметричного алгоритма блочного шифрования AES
    Шифрует строку из аргумента. Также возвращает вектор инициализации для дешифрования
    Ключ шифрования прописан в переменной среды .env
    """
    key = bytes(settings.PASSWORD_SCHOOL, 'utf-8')  # побайтовое представление ключа
    iv = urandom(16)  # инициализация рандомного побайтового 16-кратного вектора инициализации
    pass_to_crypt = pad(bytes(password, 'utf-8'), 16)  # побайтовое 16-кратное представление пароля
    obj = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)  # создание алгоритма
    db_pswrd = obj.encrypt(pass_to_crypt)  # шифрование
    return db_pswrd, iv


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class UserAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'role_is_active']

    def create(self, validated_data):  # определяем метод создания для хэширования и корректной записи в БД пароля юзера
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):  # переопределяем метод обновления для хэширования и корректной записи в БД пароля юзера
        super().update(instance, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    surname = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    middle_name = serializers.CharField(read_only=True)
    birthday = serializers.DateField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'surname', 'name', 'middle_name', 'birthday', 'phone', 'email', 'photo',
                  'is_active']

    def update(self, instance, validated_data):  # переопределяем метод обновления для хэширования и корректной записи в БД пароля юзера
        super().update(instance, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDB
        fields = '__all__'

    def validate(self, data):  # запрещаем завучу менять статус is_active в patch методе
        if self.context['request'].method == 'PATCH' and not self.context['request'].user.is_superuser:
            data['is_active'] = True
        return data



# class RoleAdminSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(write_only=True)
#     school_id = serializers.IntegerField(write_only=True)
#
#     class Meta:
#         model = Role
#         fields = '__all__'
#         depth = 1  # ВАЖНО! обязательно инициализировать depth, иначе сериализатор не сопоставит переменную user_id с моделью User и полем id (тоже самое school)
#
#     def validate(self, data):
#         if self.context['request'].method == 'POST':
#             print(data)
#             if not User.objects.filter(id=data['user_id']).exists() or not SchoolDB.objects.filter(
#                     id=data['school_id']).exists():
#                 raise serializers.ValidationError("Wrong User's id or School's id")
#             if Role.objects.filter(staff=data["staff"], school__id=data["school_id"],
#                                    user__id=data["user_id"]).exists():
#                 raise serializers.ValidationError("Already exists")
#             return data


# class RoleSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Role
#         exclude = ['is_active']
