import datetime

from os import urandom

from django.conf import settings
from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .models import Object, Cabinet, Class, Group, Lesson, TimeLesson, Schedule, StudentClass, StudentGroup

from main_app.models import User, SchoolDB
from main_app.serializers import UserSerializer

from roles.models import Director, Tutor, Teacher, FacultativeTeacher, Student
from roles.serializers import TutorSerializer, TeacherSerializer, FacultativeTeacherSerializer, StudentSerializer


class ObjectSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(required=True)

    class Meta:
        model = Object
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if data.get('school_id'):
            if not SchoolDB.objects.filter(id=data.get('school_id')).exists():
                raise ParseError([{"title": "schoolIsNotExist", "description": "школы с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school__id=data.get('school_id'), school__is_active=True).exists():
                raise ParseError([{"title": "invalidSchoolId", "description": "Завуч не может менять id школы на тот, где он не является активным завучем активной школы"}])

        if data.get('name'):
            if data.get('school_id') and Object.objects.filter(name=data.get('name'), school__id=data.get('school_id')).exists():
                raise ParseError([{"title": "objectExist", "description": "такой предмет уже существует в этой школе"}])
            if not data.get('school_id') and Object.objects.filter(name=data.get('name'), school=self.instance.school).exists():
                raise ParseError([{"title": "objectExist", "description": "такой предмет уже существует в этой школе"}])
        return data


class CabinetSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(required=True)

    class Meta:
        model = Cabinet
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if data.get('school_id'):
            if not SchoolDB.objects.filter(id=data.get('school_id')).exists():
                raise ParseError([{"title": "schoolIsNotExist", "description": "школы с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school__id=data.get('school_id'), school__is_active=True).exists():
                raise ParseError([{"title": "invalidSchoolId", "description": "Завуч не может менять id школы на тот, где он не является активным завучем активной школы"}])

        if data.get('name'):
            if data.get('school_id') and Cabinet.objects.filter(name=data.get('name'), school__id=data.get('school_id')).exists():
                raise ParseError([{"title": "objectExist", "description": "такой предмет уже существует в этой школе"}])
            if not data.get('school_id') and Cabinet.objects.filter(name=data.get('name'), school=self.instance.school).exists():
                raise ParseError([{"title": "objectExist", "description": "такой предмет уже существует в этой школе"}])
        return data


class ClassSerializer(serializers.ModelSerializer):
    tutor_id = serializers.IntegerField(required=True)
    cabinet_id = serializers.IntegerField(required=True)
    tutor = TutorSerializer(required=False)


    class Meta:
        model = Class
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if data.get('tutor_id'):
            if not Tutor.objects.filter(id=data.get('tutor_id'), is_active=True, user__is_active=True).exists():
                raise ParseError([{"title": "tutorIsNotExist", "description": "тьютора с таким id не существует, либо пользователь или роль не активна"}])
            if not data.get('cabinet_id') and self.instance.cabinet.school != Tutor.objects.get(id=data.get('tutor_id')).school:
                raise ParseError([{"title": "invalidCabinetTutorID", "description": "кабинет и тьютор должны относиться к одной школе"}])

        if data.get('cabinet_id'):
            if not Cabinet.objects.filter(id=data.get('cabinet_id')).exists():
                raise ParseError([{"title": "cabinetIsNotExist", "description": "кабинета с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Cabinet.objects.get(id=data.get('cabinet_id')).school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidCabinetID", "description": "Завуч не может менять id кабинет на тот, который находится в школе, где он не является активным завучем активной школы"}])
            if data.get('tutor_id') and Tutor.objects.get(id=data.get('tutor_id')).school != Cabinet.objects.get(id=data.get('cabinet_id')).school:
                raise ParseError([{"title": "invalidCabinetTutorID", "description": "кабинет и тьютор должны относиться к одной школе"}])
            if not data.get('tutor_id') and self.instance.tutor.school != Cabinet.objects.get(id=data.get('cabinet_id')).school:
                raise ParseError([{"title": "invalidCabinetTutorID", "description": "кабинет и тьютор должны относиться к одной школе"}])

        if data.get('name'):
            if data.get('cabinet_id') and Class.objects.filter(name=data.get('name'), cabinet__school=Cabinet.objects.get(id=data.get('cabinet_id')).school).exists():
                raise ParseError([{"title": "classExist", "description": "такой класс уже существует в этой школе"}])
            if not data.get('cabinet_id') and Class.objects.filter(name=data.get('name'), cabinet__school=self.instance.cabinet.school).exists():
                raise ParseError([{"title": "classExist", "description": "такой класс уже существует в этой школе"}])
        return data


class GroupSerializer(serializers.ModelSerializer):  # TODO: в остальных валидаторах сериалайзеров и вьюхах сделать в таком же стиле
    school_id = serializers.IntegerField(required=False)
    cls_id = serializers.IntegerField(required=False)

    class Meta:
        model = Group
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if data.get('school_id') and data.get('cls_id'):
            raise ParseError([{"title": "notOneID", "description": "необходимо указать одно из двух: либо ID школы, либо ID класса"}])

        if data.get('school_id'):
            if not SchoolDB.objects.filter(id=data.get('school_id')).exists():
                raise ParseError([{"title": "schoolIsNotExist", "description": "школы с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school__id=data.get('school_id'), school__is_active=True).exists():
                raise ParseError([{"title": "invalidSchoolId", "description": "завуч не может указывать id школы, где он не является активным завучем активной школы"}])

        if data.get('cls_id'):
            if not Class.objects.filter(id=data.get('cls_id')).exists():
                raise ParseError([{"title": "classIsNotExist", "description": "класса с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Class.objects.get(id=data.get('cls_id')).cabinet.school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidClassId", "description": "завуч не может указывать id класса школы, где он не является активным завучем активной школы"}])

        if self.context['request'].method == 'POST':
            if not (data.get('school_id') or data.get('cls_id')):
                raise ParseError([{"title": "nullID", "description": "необходимо указать либо ID школы, либо ID класса"}])
            if data.get('school_id') and Group.objects.filter(Q(name=data.get('name'), cls__cabinet__school__id=data.get('school_id')) | Q(name=data.get('name'), school_id=data.get('school_id'))).exists():
                raise ParseError([{"title": "groupExist", "description": "такая группа уже существует в этой школе"}])
            if data.get('cls_id') and Group.objects.filter(Q(name=data.get('name'), cls__cabinet__school=Class.objects.get(id=data.get('cls_id')).cabinet.school) | Q(name=data.get('name'), school=Class.objects.get(id=data.get('cls_id')).cabinet.school)).exists():
                raise ParseError([{"title": "groupExist", "description": "такая группа уже существует в этой школе"}])

        if self.context['request'].method == 'PATCH':
            if data.get('name'):
                if data.get('school_id') and Group.objects.filter(Q(name=data.get('name'), school__id=data.get('school_id')) | Q(name=data.get('name'), cls__cabinet__school__id=data.get('school_id'))).exists():
                    raise ParseError([{"title": "groupExist", "description": "такая группа уже существует в этой школе"}])
                elif data.get('cls_id') and Group.objects.filter(name=data.get('name'), cls__cabinet__school=Class.objects.get(id=data.get('cls_id')).cabinet.school).exists():
                    raise ParseError([{"title": "groupExist", "description": "такая группа уже существует в этой школе"}])
                elif self.instance.school and Group.objects.filter(name=data.get('name'), school=self.instance.school).exists():
                    raise ParseError([{"title": "groupExist", "description": "такая группа уже существует в этой школе"}])
                elif self.instance.cls and Group.objects.filter(name=data.get('name'), cls__cabinet__school=Group.objects.get(id=self.instance.id).cls.cabinet.school).exists():
                    raise ParseError([{"title": "groupExist", "description": "такая группа уже существует в этой школе"}])

            if data.get('school_id'):
                data['cls_id'] = None

            if self.instance.school and data.get('cls_id'):  # TODO: добавить проверку на наличие учеников в группе из других классов. Если есть - в ответе отдавать список "лишних" учеников
                raise ParseError([{"title": "groupExist", "description": "невозможно заменить school_id на class_id"}])

        return data


class LessonSerializer(serializers.ModelSerializer):
    object_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField(required=False)
    facultative_teacher_id = serializers.IntegerField(required=False)
    teacher = TeacherSerializer(required=False)
    facultative_teacher = FacultativeTeacherSerializer(required=False)

    class Meta:
        model = Lesson
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if data.get('teacher_id') and data.get('facultative_teacher_id'):
            raise ParseError([{"title": "notOneID", "description": "необходимо указать одно из двух: либо ID учителя, либо ID учителя факультатива"}])

        if data.get('object_id'):
            if not Object.objects.filter(id=data.get('object_id')).exists():
                raise ParseError([{"title": "objectIsNotExist", "description": "предмета с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Object.objects.get(id=data.get('object_id')).school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidObjectId", "description": "завуч не может указывать id школы, где он не является активным завучем активной школы"}])

        if data.get('teacher_id'):
            if not Teacher.objects.filter(id=data.get('teacher_id'), is_active=True, user__is_active=True).exists():
                raise ParseError([{"title": "teacherIsNotExist", "description": "учителя с таким id не существует, либо пользователь или роль не активна"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Teacher.objects.get(id=data.get('teacher_id')).school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidTeacherId", "description": "завуч не может указывать id учителя школы, где он не является активным завучем активной школы"}])
            if data.get('object_id') and Teacher.objects.get(id=data.get('teacher_id')).school != Object.objects.get(id=data.get('object_id')).school:
                raise ParseError([{"title": "invalidObjectAndTeacherID", "description": "школы предмета и учителя должны совпадать"}])

        if data.get('facultative_teacher_id'):
            if not FacultativeTeacher.objects.filter(id=data.get('facultative_teacher_id'), is_active=True, user__is_active=True).exists():
                raise ParseError([{"title": "facultativeTeacherIsNotExist", "description": "учителя факультативов с таким id не существует, либо пользователь или роль не активна"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=FacultativeTeacher.objects.get(id=data.get('facultative_teacher_id')).school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidFacultativeTeacherId", "description": "завуч не может указывать id учителя факультативов школы, где он не является активным завучем активной школы"}])
            if data.get('object_id') and FacultativeTeacher.objects.get(id=data.get('facultative_teacher_id')).school != Object.objects.get(id=data.get('object_id')).school:
                raise ParseError([{"title": "invalidObjectAndFacultativeTeacherID", "description": "школы предмета и учителя факультативов должны совпадать"}])

        if self.context['request'].method == 'POST':
            if not (data.get('teacher_id') or data.get('facultative_teacher_id')):
                raise ParseError([{"title": "nullID", "description": "необходимо указать либо ID учителя, либо ID учителя факультативов"}])

        if self.context['request'].method == 'PATCH':
            if data.get('object_id'):
                if data.get('teacher_id'):
                    if Object.objects.get(id=data.get('object_id')) != Teacher.objects.get(id=data.get('teacher_id')).school:
                        raise ParseError([{"title": "invalidObjectAndTeacherID", "description": "школы предмета и учителя должны совпадать"}])
                    data['facultative_teacher_id'] = None
                elif data.get('facultative_teacher_id'):
                    if Object.objects.get(id=data.get('object_id')).school != FacultativeTeacher.objects.get(id=data.get('facultative_teacher_id')).school:
                        raise ParseError([{"title": "invalidObjectAndFacultativeTeacherID", "description": "школы предмета и учителя факультативов должны совпадать"}])
                    data['teacher_id'] = None
                else:
                    if self.instance.object.school != Object.objects.get(id=data.get('object_id')).school:
                        raise ParseError([{"title": "invalidObjectSchool", "description": "школы старого и нового предметов должны совпадать (если без замены учителя или учителя факультативов)"}])

            else:
                if data.get('teacher_id'):
                    if self.instance.object.school != Teacher.objects.get(id=data.get('teacher_id')).school:
                        raise ParseError([{"title": "invalidObjectAndTeacherID", "description": "школы предмета и учителя должны совпадать"}])
                    data['facultative_teacher_id'] = None
                elif data.get('facultative_teacher_id'):
                    if self.instance.object.school != FacultativeTeacher.objects.get(id=data.get('facultative_teacher_id')).school:
                        raise ParseError([{"title": "invalidObjectAndFacultativeTeacherID", "description": "школы предмета и учителя факультативов должны совпадать"}])
                    data['teacher_id'] = None

        return data


class TimeLessonSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(required=True)

    class Meta:
        model = TimeLesson
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if data.get('school_id'):
            if not SchoolDB.objects.filter(id=data.get('school_id')).exists():
                raise ParseError([{"title": "schoolIsNotExist", "description": "школы с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school__id=data.get('school_id'), school__is_active=True).exists():
                raise ParseError([{"title": "invalidSchoolId", "description": "Завуч не может менять id школы на тот, где он не является активным завучем активной школы"}])
            if data.get('period') and TimeLesson.objects.filter(period=data.get('period'), school_id=data.get('school_id')).exists():
                raise ParseError([{"title": "periodExist", "description": "такой период действия расписания уроков уже существует в этой школе"}])

        else:
            if data.get('period') and TimeLesson.objects.filter(period=data.get('period'), school=self.instance.school).exists():
                raise ParseError([{"title": "periodExist", "description": "такой период действия расписания уроков уже существует в этой школе"}])

        i = 1

        while i <= 10:
            if data.get(f"lesson{i}_end"):
                if data.get(f"lesson{i}_start") and data.get(f"lesson{i}_start") > data.get(f"lesson{i}_end"):
                    raise ParseError([{"title": "invalidTimeLessons", "description": "Окончание урока не может быть раньше его начала"}])
                if data.get(f"lesson{i+1}_start") and data.get(f"lesson{i}_end") > data.get(f"lesson{i+1}_start"):
                    raise ParseError([{"title": "invalidTimeLessons", "description": "Начало следующего урока не может быть раньше окончания предыдущего"}])
                if self.instance:
                    if not data.get(f"lesson{i}_start") and getattr(self.instance, f"lesson{i}_start", datetime.time()) > data.get(f"lesson{i}_end"):
                        raise ParseError([{"title": "invalidTimeLessons", "description": "Окончание урока не может быть раньше его начала"}])
                    if i < 10 and not data.get(f"lesson{i+1}_start") and data.get(f"lesson{i}_end") > getattr(self.instance, f"lesson{i+1}_start", datetime.time()):
                        raise ParseError([{"title": "invalidTimeLessons", "description": "Начало следующего урока не может быть раньше окончания предыдущего"}])
            if data.get(f"lesson{i}_start") and self.instance:
                if not data.get(f"lesson{i}_end") and getattr(self.instance, f"lesson{i}_end", datetime.time()) < data.get(f"lesson{i}_start"):
                    raise ParseError([{"title": "invalidTimeLessons", "description": "Окончание урока не может быть раньше его начала"}])
                if not data.get(f"lesson{i-1}_end") and getattr(self.instance, f"lesson{i-1}_end", datetime.time()) > data.get(f"lesson{i}_start"):
                    raise ParseError([{"title": "invalidTimeLessons", "description": "Начало следующего урока не может быть раньше окончания предыдущего"}])
            i += 1
        return data


class ScheduleSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField()
    lesson_replace_id = serializers.IntegerField(required=False)
    lesson = LessonSerializer(required=False)
    lesson_replace = LessonSerializer(required=False)
    student_id = serializers.IntegerField(required=False)
    group_id = serializers.IntegerField(required=False)
    cls_id = serializers.IntegerField(required=False)
    cabinet_id = serializers.IntegerField(required=False)
    time_lesson_id = serializers.IntegerField(required=False)

    class Meta:
        model = Schedule
        fields = '__all__'
        depth = 1

    def validate(self, data):
        student = (1 if data.get('student_id') else 0)
        group = (1 if data.get('group_id') else 0)
        cls = (1 if data.get('cls_id') else 0)
        start = (data.get('start') if data.get('start') else self.instance.start)
        end = (data.get('end') if data.get('start') else self.instance.end)

        if data.get('lesson_id'):
            if not Lesson.objects.filter(id=data.get('lesson_id')).exists():
                raise ParseError([{"title": "lessonIsNotExist", "description": "урока с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Lesson.objects.get(id=data.get('lesson_id')).object.school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidLessonId", "description": "завуч не может указывать id урока в школе, где он не является активным завучем активной школы"}])
            if data.get('lesson_replace_id') and Lesson.objects.get(id=data.get('lesson_id')).object.school != Lesson.objects.get(id=data.get('lesson_replace_id')).object.school:
                raise ParseError([{"title": "differentLessonSchool", "description": "школы у lesson и lesson_replace должны совпадать"}])
        if data.get('lesson_replace_id'):
            if not Lesson.objects.filter(id=data.get('lesson_replace_id')).exists():
                raise ParseError([{"title": "lessonReplaceIsNotExist", "description": "замены урока с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Lesson.objects.get(id=data.get('lesson_replace_id')).object.school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidLessonReplaceId", "description": "завуч не может указывать id замены урока в школе, где он не является активным завучем активной школы"}])
        if data.get('student_id'):
            if not Student.objects.filter(id=data.get('student_id')).exists():
                raise ParseError([{"title": "studentIsNotExist", "description": "ученика с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Student.objects.get(id=data.get('student_id')).school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidStudentId", "description": "завуч не может указывать id ученика в школе, где он не является активным завучем активной школы"}])
        if data.get('group_id'):
            if not Group.objects.filter(id=data.get('group_id')).exists():
                raise ParseError([{"title": "groupIsNotExist", "description": "группы с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=(Group.objects.get(id=data.get('group_id')).school if getattr(Group.objects.get(id=data.get('group_id')), 'school', 0) else Group.objects.get(id=data.get('group_id')).cls.cabinet.school), school__is_active=True).exists():
                raise ParseError([{"title": "invalidGroupId", "description": "завуч не может указывать id группы в школе, где он не является активным завучем активной школы"}])
        if data.get('cls_id'):
            if not Class.objects.filter(id=data.get('cls_id')).exists():
                raise ParseError([{"title": "classIsNotExist", "description": "класса с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Class.objects.get(id=data.get('cls_id')).cabinet.school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidClassId", "description": "завуч не может указывать id класса в школе, где он не является активным завучем активной школы"}])
        if data.get('cabinet_id'):
            if not Cabinet.objects.filter(id=data.get('cabinet_id')).exists():
                raise ParseError([{"title": "cabinetIsNotExist", "description": "кабинета с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=Cabinet.objects.get(id=data.get('cabinet_id')).school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidCabinetId", "description": "завуч не может указывать id кабинета в школе, где он не является активным завучем активной школы"}])
        if data.get('number') and (1 > data.get('number') or data.get('number') > 10):
            raise ParseError([{"title": "invalidNumber", "description": "номер урока должен быть от 1 до 10"}])

        if data.get('start') and data.get('end') and data.get('start') > data.get('end'):
            raise ParseError([{"title": "invalidTime", "description": "Начало урока не может быть раньше окончания"}])
        if data.get('time_lesson_id'):
            if not TimeLesson.objects.filter(id=data.get('time_lesson_id')).exists():
                raise ParseError([{"title": "timeLessonIsNotExist", "description": "времени уроков с таким id не существует"}])
            if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True, school=TimeLesson.objects.get(id=data.get('time_lesson_id')).school, school__is_active=True).exists():
                raise ParseError([{"title": "invalidCabinetId", "description": "завуч не может указывать id времени уроков в школе, где он не является активным завучем активной школы"}])

        if self.context['request'].method == 'POST':
            school = Lesson.objects.get(id=data.get('lesson_id')).object.school
            if (student + group + cls) != 1:
                raise ParseError([{"title": "notOneID", "description": "необходимо указать одно и только одно из трех: либо ID ученика, либо ID группы, либо ID класса"}])
            if data.get('time_lesson_id') and TimeLesson.objects.get(id=data.get('time_lesson_id')).school != school:
                raise ParseError([{"title": "invalidLessonTimeLessonId", "description": "школы, связанные с уроком и временем расписания уроков должны совпадать"}])
            if data.get('cabinet_id') and Cabinet.objects.get(id=data.get('cabinet_id')).school != school:
                raise ParseError([{"title": "invalidCabinetLessonId", "description": "школы, связанные с уроком и кабинетом должны совпадать"}])
            if student:
                if Student.objects.get(id=data.get('student_id')).school != school:
                    raise ParseError([{"title": "invalidLessonStudentId", "description": "школы, связанные с уроком и учеником должны совпадать"}])
                if Schedule.objects.filter(start__lte=start, end__gte=start, student__id=data.get('student_id')):
                    raise ParseError([{"title": "scheduleExist", "description": "урок для этого ученика в это время уже существует"}])
            if cls:
                if Class.objects.get(id=data.get('cls_id')).cabinet.school != school:
                    raise ParseError([{"title": "invalidLessonClassId", "description": "школы, связанные с уроком и классом должны совпадать"}])
                if Schedule.objects.filter(start__lte=start, end__gte=start, cls__id=data.get('cls_id')):
                    raise ParseError([{"title": "scheduleExist", "description": "урок для этого класса в это время уже существует"}])
            if group:
                if (Group.objects.get(id=data.get('group_id')).school if getattr(Group.objects.get(id=data.get('group_id')), 'school', 0) else Group.objects.get(id=data.get('group_id')).cls.cabinet.school) != school:
                    raise ParseError([{"title": "invalidLessonGroupId", "description": "школы, связанные с уроком и группой должны совпадать"}])
                if Schedule.objects.filter(start__lte=start, end__gte=start, group__id=data.get('group_id')):
                    raise ParseError([{"title": "scheduleExist", "description": "урок для этой группы в это время уже существует"}])
            if not data.get('cabinet_id'):
                if data.get('cls_id'):
                    data['cabinet_id'] = Class.objects.get(id=data.get('cls_id')).cabinet.id
                    data['cabinet'] = Class.objects.get(id=data.get('cls_id')).cabinet
                else:
                    raise ParseError([{"title": "cabinetIsNull", "description": "указание кабинета обязательно, если расписание для ученика или группы"}])
            if data.get('time_lesson_id') and not data.get('number'):
                raise ParseError([{"title": "numberIsNull", "description": "указание номера урока обязательно, если шаблонное расписание для ученика или группы"}])

        if self.context['request'].method == 'PATCH':
            if self.instance.time_lesson:
                if data.get('start') and not data.get('end'):
                    if data.get('number') and data.get('start') > getattr(self.instance.time_lesson, f"lesson{data.get('number')}_end"):
                        raise ParseError([{"title": "invalidTime", "description": "Начало урока не может быть раньше окончания"}])
                    if not data.get('number') and data.get('start') > getattr(self.instance.time_lesson, f"lesson{self.instance.number}_end"):
                        raise ParseError([{"title": "invalidTime", "description": "Начало урока не может быть раньше окончания"}])
                if data.get('end') and not data.get('start'):
                    if data.get('number') and data.get('end') < getattr(self.instance.time_lesson, f"lesson{data.get('number')}_start"):
                        raise ParseError([{"title": "invalidTime", "description": "Начало урока не может быть раньше окончания"}])
                    if not data.get('number') and data.get('end') < getattr(self.instance.time_lesson, f"lesson{self.instance.number}_start"):
                        raise ParseError([{"title": "invalidTime", "description": "Начало урока не может быть раньше окончания"}])

            school = (Lesson.objects.get(id=data.get('lesson_id')).object.school if data.get('lesson_id') else self.instance.lesson.object.school)
            if (student + group + cls) > 1:
                raise ParseError([{"title": "moreThanOneID", "description": "необходимо указать не больше одного: либо ID ученика, либо ID группы, либо ID класса"}])
            if data.get('time_lesson_id') and TimeLesson.objects.get(id=data.get('time_lesson_id')).school != school:
                raise ParseError([{"title": "invalidLessonTimeLessonId", "description": "школы, связанные с уроком и временем расписания уроков должны совпадать"}])
            if data.get('cabinet_id') and Cabinet.objects.get(id=data.get('cabinet_id')).school != school:
                raise ParseError([{"title": "invalidCabinetLessonId", "description": "школы, связанные с уроком и кабинетом должны совпадать"}])
            if student:
                if Student.objects.get(id=data.get('student_id')).school != school:
                    raise ParseError([{"title": "invalidLessonStudentId", "description": "школы, связанные с уроком и учеником должны совпадать"}])
                if Schedule.objects.filter(start__lte=start, end__gte=start, student__id=data.get('student_id')):
                    raise ParseError([{"title": "scheduleExist", "description": "урок для этого ученика в это время уже существует"}])
                data['group_id'] = None
                data['cls_id'] = None
            if cls:
                if Class.objects.get(id=data.get('cls_id')).cabinet.school != school:
                    raise ParseError([{"title": "invalidLessonClassId", "description": "школы, связанные с уроком и классом должны совпадать"}])
                if Schedule.objects.filter(start__lte=start, end__gte=start, cls__id=data.get('cls_id')):
                    raise ParseError([{"title": "scheduleExist", "description": "урок для этого класса в это время уже существует"}])
                data['group_id'] = None
                data['student_id'] = None
            if group:
                if (Group.objects.get(id=data.get('group_id')).school if getattr(Group.objects.get(id=data.get('group_id')), 'school', 0) else Group.objects.get(id=data.get('group_id')).cls.cabinet.school) != school:
                    raise ParseError([{"title": "invalidLessonGroupId", "description": "школы, связанные с уроком и группой должны совпадать"}])
                if Schedule.objects.filter(start__lte=start, end__gte=start, group__id=data.get('group_id')):
                    raise ParseError([{"title": "scheduleExist", "description": "урок для этой группы в это время уже существует"}])
                data['cls_id'] = None
                data['student_id'] = None
            if data.get('lesson_replace_id'):
                if data.get('lesson_id') and Lesson.objects.get(id=data.get('lesson_id')).object.school != Lesson.objects.get(id=data.get('lesson_replace_id')).object.school:
                    raise ParseError([{"title": "differentLessonSchool", "description": "школы у lesson и lesson_replace должны совпадать"}])
                if not data.get('lesson_id') and self.instance.lesson.object.school != Lesson.objects.get(id=data.get('lesson_replace_id')).object.school:
                    raise ParseError([{"title": "differentLessonSchool", "description": "школы у lesson и lesson_replace должны совпадать"}])


        return data


class StudentClassSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)
    student_id = serializers.IntegerField()
    cls = ClassSerializer(required=False)
    cls_id = serializers.IntegerField()

    class Meta:
        model = StudentClass
        fields = '__all__'
        depth = 2  # увеличиваем "глубину" отображения связанных сущностей

    def validate(self, data):
        """
        Проверка валидности request данных при POST / PATCH запросах
        """

        if data.get('cls_id'):
            if not Class.objects.filter(id=data['cls_id']).exists():
                raise ParseError([{"title": "invalidClsId", "description": "не верно указан id класса"}])

        if data.get('student_id'):
            if not Student.objects.filter(id=data['student_id']).exists():
                raise ParseError([{"title": "invalidStudentId", "description": "не верно указан id ученика"}])
            if StudentClass.objects.filter(student__id=data['student_id']).exists():
                raise ParseError([{"title": "studentIdExists", "description": "у ученика уже есть связь с классом"}])
            if data.get('cls_id'):
                if Class.objects.get(id=data['cls_id']).cabinet.school != Student.objects.get(id=data['student_id']).school:
                    raise ParseError([{"title": "differentSchools", "description": "школы ученика и класса должны совпадать"}])
                if not self.context['request'].user.is_superuser and not Director.objects.filter(
                        user=self.context['request'].user, is_active=True, school=Student.objects.get(id=data['student_id']).school, school__is_active=True).exists():
                    raise ParseError([{"title": "permissionDenied", "description": "активный завуч может создавать записи только для учеников и классов своей активной школы"}])
            else:
                if self.instance.cls.cabinet.school != Student.objects.get(id=data['student_id']).school:
                    raise ParseError([{"title": "differentSchools", "description": "школы ученика и класса должны совпадать"}])
        elif data.get('cls_id'):
            if self.instance.student.school != Class.objects.get(id=data['cls_id']).cabinet.school:
                raise ParseError([{"title": "differentSchools", "description": "школы ученика и класса должны совпадать"}])

        return data


class StudentGroupSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)
    student_id = serializers.IntegerField()
    group = GroupSerializer(required=False)
    group_id = serializers.IntegerField()

    class Meta:
        model = StudentGroup
        fields = '__all__'
        depth = 2  # увеличиваем "глубину" отображения связанных сущностей

    def validate(self, data):
        """
        Проверка валидности request данных при POST / PATCH запросах
        """

        if data.get('group_id'):
            if not Group.objects.filter(id=data['group_id']).exists():
                raise ParseError([{"title": "invalidGroupId", "description": "не верно указан id группы"}])

        if data.get('student_id'):
            if not Student.objects.filter(id=data['student_id']).exists():
                raise ParseError([{"title": "invalidStudentId", "description": "не верно указан id ученика"}])
            if data.get('group_id'):
                if (Group.objects.get(id=data['group_id']).cls.cabinet.school if getattr(Group.objects.get(id=data['group_id']), "cls") else Group.objects.get(id=data['group_id']).school) != Student.objects.get(id=data['student_id']).school:
                    raise ParseError([{"title": "differentSchools", "description": "школы ученика и группы должны совпадать"}])
                if not self.context['request'].user.is_superuser and not Director.objects.filter(user=self.context['request'].user, is_active=True,
                                                                                                 school=Student.objects.get(id=data['student_id']).school, school__is_active=True).exists():
                    raise ParseError([{"title": "permissionDenied", "description": "активный завуч может создавать записи только для учеников и групп своей активной школы"}])
                if StudentGroup.objects.filter(student__id=data['student_id'], group__id=data['group_id']).exists():
                    raise ParseError([{"title": "studentIdExists", "description": "у ученика уже есть такая связь с группой"}])
            else:
                if self.instance.student.school != Student.objects.get(id=data['student_id']).school:
                    raise ParseError([{"title": "differentSchools", "description": "школы ученика и группы должны совпадать"}])
        elif data.get('group_id'):
            if self.instance.student.school != (Group.objects.get(id=data['group_id']).cls.cabinet.school if getattr(Group.objects.get(id=data['group_id']), "cls") else Group.objects.get(id=data['group_id']).school):
                raise ParseError([{"title": "differentSchools", "description": "школы ученика и группы должны совпадать"}])

        return data
