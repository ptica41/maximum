from os import urandom

from django.conf import settings

from rest_framework import serializers

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .models import Director, Teacher, FacultativeTeacher, Tutor, Parent, Student, Food, ParentChild

from main_app.models import User, SchoolDB
from main_app.serializers import UserSerializer


class DirectorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()

    class Meta:
        model = Director
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if not self.context['request'].user.is_superuser and 'user_id' in data and not User.objects.filter(id=data['user_id'], is_active=True).exists():
            raise serializers.ValidationError('Не верный id пользователя либо неактивный пользователь')
        if 'user_id' in data and not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError('Не верный id пользователя')
        if 'school_id' in data and not SchoolDB.objects.filter(id=data['school_id']).exists():
            raise serializers.ValidationError('Не верный id школы')
        if 'user_id' in data and 'school_id' in data and Director.objects.filter(user__id=data['user_id'], school__id=data['school_id']).exists():
            raise serializers.ValidationError('Запись с данными id user и school уже существует!')
        return data


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()

    class Meta:
        model = Teacher
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if not self.context['request'].user.is_superuser and 'user_id' in data and not User.objects.filter(id=data['user_id'], is_active=True).exists():
            raise serializers.ValidationError('Не верный id пользователя либо неактивный пользователь')
        if 'user_id' in data and not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError('Не верный id пользователя')
        if 'school_id' in data and not SchoolDB.objects.filter(id=data['school_id']).exists():
            raise serializers.ValidationError('Не верный id школы')
        if 'user_id' in data and 'school_id' in data and Teacher.objects.filter(user__id=data['user_id'], school__id=data['school_id']).exists():
            raise serializers.ValidationError('Запись с данными id user и school уже существует!')
        return data


class FacultativeTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()

    class Meta:
        model = FacultativeTeacher
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if not self.context['request'].user.is_superuser and 'user_id' in data and not User.objects.filter(id=data['user_id'], is_active=True).exists():
            raise serializers.ValidationError('Не верный id пользователя либо неактивный пользователь')
        if 'user_id' in data and not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError('Не верный id пользователя')
        if 'school_id' in data and not SchoolDB.objects.filter(id=data['school_id']).exists():
            raise serializers.ValidationError('Не верный id школы')
        if 'user_id' in data and 'school_id' in data and FacultativeTeacher.objects.filter(user__id=data['user_id'], school__id=data['school_id']).exists():
            raise serializers.ValidationError('Запись с данными id user и school уже существует!')
        return data


class TutorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()

    class Meta:
        model = Tutor
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if not self.context['request'].user.is_superuser and 'user_id' in data and not User.objects.filter(id=data['user_id'], is_active=True).exists():
            raise serializers.ValidationError('Не верный id пользователя либо неактивный пользователь')
        if 'user_id' in data and not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError('Не верный id пользователя')
        if 'school_id' in data and not SchoolDB.objects.filter(id=data['school_id']).exists():
            raise serializers.ValidationError('Не верный id школы')
        if 'user_id' in data and 'school_id' in data and Tutor.objects.filter(user__id=data['user_id'], school__id=data['school_id']).exists():
            raise serializers.ValidationError('Запись с данными id user и school уже существует!')
        return data


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()

    class Meta:
        model = Parent
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if not self.context['request'].user.is_superuser and 'user_id' in data and not User.objects.filter(id=data['user_id'], is_active=True).exists():
            raise serializers.ValidationError('Не верный id пользователя либо неактивный пользователь')
        if 'user_id' in data and not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError('Не верный id пользователя')
        if 'school_id' in data and not SchoolDB.objects.filter(id=data['school_id']).exists():
            raise serializers.ValidationError('Не верный id школы')
        if 'user_id' in data and 'school_id' in data and Parent.objects.filter(user__id=data['user_id'], school__id=data['school_id']).exists():
            raise serializers.ValidationError('Запись с данными id user и school уже существует!')
        return data


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()

    class Meta:
        model = Student
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if not self.context['request'].user.is_superuser and 'user_id' in data and not User.objects.filter(id=data['user_id'], is_active=True).exists():
            raise serializers.ValidationError('Не верный id пользователя либо неактивный пользователь')
        if 'user_id' in data and not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError('Не верный id пользователя')
        if 'school_id' in data and not SchoolDB.objects.filter(id=data['school_id']).exists():
            raise serializers.ValidationError('Не верный id школы')
        if 'user_id' in data and 'school_id' in data and Student.objects.filter(user__id=data['user_id'], school__id=data['school_id']).exists():
            raise serializers.ValidationError('Запись с данными id user и school уже существует!')
        return data


class FoodSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()

    class Meta:
        model = Food
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if not self.context['request'].user.is_superuser and 'user_id' in data and not User.objects.filter(id=data['user_id'], is_active=True).exists():
            raise serializers.ValidationError('Не верный id пользователя либо неактивный пользователь')
        if 'user_id' in data and not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError('Не верный id пользователя')
        if 'school_id' in data and not SchoolDB.objects.filter(id=data['school_id']).exists():
            raise serializers.ValidationError('Не верный id школы')
        if 'user_id' in data and 'school_id' in data and Food.objects.filter(user__id=data['user_id'], school__id=data['school_id']).exists():
            raise serializers.ValidationError('Запись с данными id user и school уже существует!')
        return data


class ParentChildSerializer(serializers.ModelSerializer):
    """
    TODO: ИСПРАВИТЬ ВАЛИДАЦИЮ
    """
    child = StudentSerializer(required=False)
    child_id = serializers.IntegerField()
    parent = ParentSerializer(required=False)
    parent_id = serializers.IntegerField()

    class Meta:
        model = ParentChild
        fields = '__all__'
        depth = 2  # увеличиваем "глубину" отображения связанных сущностей

    def validate(self, data):
        """
        Проверка валидности request данных при POST / PATCH запросах
        """
        if self.context['request'].method == 'POST':
            if not Parent.objects.filter(id=data['parent_id']).exists() or not Student.objects.filter(id=data['child_id']).exists():
                raise serializers.ValidationError("Wrong Parent's id or Child's id")
            if ParentChild.objects.filter(child__id=data['child_id'], parent__id=data['parent_id']).exists():
                raise serializers.ValidationError("Already exists")
            if ParentChild.objects.filter(child__id=data['child_id']).exists():
                raise serializers.ValidationError("Parent for this child already exist")
            if data['parent_id'] == data['child_id']:
                raise serializers.ValidationError("Parent_id and child_id cannot be the same")
            if Parent.objects.get(id=data['parent_id']).school != Student.objects.get(id=data['child_id']).school:
                raise serializers.ValidationError("Parent's school and child's school must be the same")

        if self.context['request'].method == 'PATCH':
            if 'parent_id' in data:
                if not Parent.objects.filter(id=data['parent_id']).exists():
                    raise serializers.ValidationError("Wrong Parent's id")
                # if not Parent.objects.get(id=data['parent_id']).user.is_active:
                #     raise serializers.ValidationError("Parent's user isn't active")
                if 'child_id' not in data:
                    if Parent.objects.get(id=data['parent_id']).school != self.instance.child.school:
                        raise serializers.ValidationError("Parent's school and child's school must be the same")


            if 'child_id' in data:
                if not Student.objects.filter(id=data['child_id']).exists():
                    raise serializers.ValidationError("Wrong Child's id")
                # if not Student.objects.get(id=data['child_id']).user.is_active:
                #     raise serializers.ValidationError("Child's user isn't active")
                if ParentChild.objects.filter(child__id=data['child_id']).exists() and data['child_id'] != self.instance.child.id:
                    raise serializers.ValidationError("Parent for this child already exist")
                if 'parent_id' not in data:
                    if Student.objects.get(id=data['child_id']).school != self.instance.parent.school:
                        raise serializers.ValidationError("Parent's school and child's school must be the same")

            if 'parent_id' in data and 'child_id' in data:
                if ParentChild.objects.filter(child__id=data['child_id'], parent__id=data['parent_id']).exists() and data['child_id'] != self.instance.child.id and data['parent_id'] != self.instance.parent.id:
                    raise serializers.ValidationError("Already exists")
                if Parent.objects.get(id=data['parent_id']).user == Student.objects.get(id=data['child_id']).user:
                    raise serializers.ValidationError("Parent as user and child as user cannot be the same")
                if Parent.objects.get(id=data['parent_id']).school != Student.objects.get(id=data['child_id']).school:
                    raise serializers.ValidationError("Parent's school and child's school must be the same")

        return data
