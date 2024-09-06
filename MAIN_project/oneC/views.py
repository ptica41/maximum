from django.conf import settings

from rest_framework import serializers, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Partner1C, ParentChild1C
from .serializers import Partner1CSerializer, ParentChild1CSerializer

from main_app.views import IsActive, CustomJWTAuthentication
# from main_app.models import Role


def clean_FIO(data: str):
    """
    Функция возвращает фамилию, имя, отчество, пол полученные из строковой записи ФИО без ненужных пробелов
    TODO: доработать нестандартные случаи (например "оглы" у азербайджанцев)
    """
    MALE = ['Авдей', 'Авксентий', 'Агапит', 'Агафон', 'Акакий', 'Акиндин', 'Александр', 'Алексей', 'Альберт',
            'Анатолий', 'Андрей', 'Аникий', 'Аникита', 'Антон', 'Антонин', 'Анфим', 'Аристарх', 'Аркадий', 'Арсений',
            'Артём', 'Артемий', 'Артур', 'Архипп', 'Афанасий', 'Богдан', 'Борис', 'Вавила', 'Вадим', 'Валентин',
            'Валерий', 'Валерьян', 'Варлам', 'Варсонофий', 'Варфоломей', 'Василий', 'Венедикт', 'Вениамин', 'Викентий',
            'Виктор', 'Виссарион', 'Виталий', 'Владимир', 'Владислав', 'Владлен', 'Влас', 'Всеволод', 'Вячеслав',
            'Гавриил', 'Галактион', 'Геласий', 'Геннадий', 'Георгий', 'Герасим', 'Герман', 'Германн', 'Глеб', 'Гордей',
            'Григорий', 'Данакт', 'Даниил', 'Данил', 'Данила', 'Демид', 'Демьян', 'Денис', 'Дмитрий', 'Добрыня',
            'Донат', 'Дорофей', 'Евгений', 'Евграф', 'Евдоким', 'Евсей', 'Евстафий', 'Егор', 'Емельян', 'Еремей',
            'Ермолай', 'Ерофей', 'Ефим', 'Ефрем', 'Ждан', 'Зиновий', 'Иакинф', 'Иван', 'Игнатий', 'Игорь', 'Изот',
            'Илья', 'Иннокентий', 'Ираклий', 'Ириней', 'Исаак', 'Исидор', 'Иуда', 'Иулиан', 'Капитон', 'Ким', 'Кир',
            'Кирилл', 'Климент', 'Кондрат', 'Конон', 'Константин', 'Корнилий', 'Кузьма', 'Куприян', 'Лаврентий', 'Лев',
            'Леонид', 'Леонтий', 'Логгин', 'Лука', 'Лукий', 'Лукьян', 'Магистриан', 'Макар', 'Максим', 'Мамонт', 'Марк',
            'Мартын', 'Матвей', 'Мелентий', 'Мина', 'Мирослав', 'Митрофан', 'Михаил', 'Мстислав', 'Назар', 'Нестор',
            'Никандр', 'Никанор', 'Никита', 'Никифор', 'Никодим', 'Николай', 'Никон', 'Олег', 'Онисим', 'Онуфрий',
            'Павел', 'Паисий', 'Панкратий', 'Пантелеймон', 'Парфений', 'Пафнутий', 'Пахомий', 'Пётр', 'Платон',
            'Поликарп', 'Порфирий', 'Потап', 'Пров', 'Прокопий', 'Протасий', 'Прохор', 'Разумник', 'Родион', 'Роман',
            'Ростислав', 'Руслан', 'Савва', 'Савелий', 'Самуил', 'Святополк', 'Святослав', 'Севастьян', 'Семён',
            'Серафим', 'Сергей', 'Сила', 'Сильвестр', 'Созон', 'Софрон', 'Спиридон', 'Станислав', 'Степан', 'Тарас',
            'Тимофей', 'Тимур', 'Тит', 'Тихон', 'Трифон', 'Трофим', 'Урбан', 'Фаддей', 'Фёдор', 'Федосей', 'Федот',
            'Феликс', 'Феоктист', 'Филат', 'Филимон', 'Филипп', 'Фирс', 'Фока', 'Фома', 'Фотий', 'Фрол', 'Харитон',
            'Хрисанф', 'Христофор', 'Эдуард', 'Эраст', 'Юлиан', 'Юрий', 'Юстин', 'Яков', 'Якун', 'Ян', 'Ярослав']

    FEMALE = ['Агафья', 'Аглая', 'Агриппина', 'Аза', 'Акулина', 'Алевтина', 'Александра', 'Алина', 'Алиса', 'Алла',
              'Анастасия', 'Ангелина', 'Анжела', 'Анжелика', 'Анна', 'Антонина', 'Анфиса', 'Валентина', 'Валерия',
              'Варвара', 'Василиса', 'Вера', 'Вероника', 'Виктория', 'Владимира', 'Галина', 'Глафира', 'Гликерия',
              'Дана', 'Дарья', 'Ева', 'Евгения', 'Евдокия', 'Евлалия', 'Евлампия', 'Евпраксия', 'Евфросиния',
              'Екатерина', 'Елена', 'Елизавета', 'Епистима', 'Ермиония', 'Жанна', 'Зинаида', 'Злата', 'Зоя', 'Инга',
              'Инесса', 'Инна', 'Иоанна', 'Ираида', 'Ирина', 'Капитолина', 'Карина', 'Каролина', 'Кира', 'Клавдия',
              'Ксения', 'Лада', 'Лариса', 'Лидия', 'Лилия', 'Любовь', 'Людмила', 'Маргарита', 'Марина', 'Мария',
              'Марфа', 'Матрёна', 'Милица', 'Мирослава', 'Надежда', 'Наталья', 'Нина', 'Нонна', 'Оксана', 'Октябрина',
              'Олеся', 'Олимпиада', 'Ольга', 'Павлина', 'Пелагея', 'Пинна', 'Полина', 'Прасковья', 'Рада', 'Раиса',
              'Регина', 'Римма', 'Рогнеда', 'Светлана', 'Серафима', 'Снежана', 'София', 'Сусанна', 'Таисия', 'Тамара',
              'Татьяна', 'Улита', 'Ульяна', 'Урсула', 'Фаина', 'Феврония', 'Фёкла', 'Феодора', 'Элеонора', 'Юлия',
              'Яна', 'Ярослава']

    data = data.replace('  ', ' ')  # удаляем двойные пробелы

    if data and data[0] == ' ':  # удаляем пробел вначале
        data = data[1:]

    surname = data.split(' ')[0]  # записываем фамилию

    try:
        name = data.split(' ')[1]  # записываем имя
    except IndexError:
        name = None

    try:
        middle_name = data.split(' ')[2]  # записываем отчество
    except IndexError:
        middle_name = None

    # определяем пол по окончанию отчества или соответствии имени значению из списка имен
    if (middle_name and middle_name[-2:] in ['на']) or (
            not middle_name and name in FEMALE):
        male = 'FEMALE'
    elif (middle_name and middle_name[-2:] in ['ич']) or (
            not middle_name and name in MALE):
        male = 'MALE'
    else:
        male = None

    return surname, name, middle_name, male


def get_birthday(data: str):
    """
    Определяем дату рождения (без времени)
    """
    birthday = (data if data and data != '0001-01-01T00:00:00' else None)
    if birthday:
        birthday = birthday.split('T')[0]
    return birthday


class ParentChildAPIView(APIView):
    """
    Добавление данных родители-дети из 1С в БД
    Доступ только у пользователя с логином "1С"
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if request.user.username == '1C':
            users = request.data['students_parents']

            for user in users:
                child_surname, child_name, child_middle_name, child_male = clean_FIO(user['students_name'])
                parent_surname, parent_name, parent_middle_name, parent_male = clean_FIO(user['parent_name'])

                child_birthday = get_birthday(user['students_document_birthDate'])
                parent_birthday = get_birthday(user['parent_document_birthDate'])

                parent_phone = (user['parent_phone'] if user['parent_phone'] else None)

                child_passport_series = (
                    user['students_document_series'] if 'Паспорт' in user['students_document'] else None)
                if child_passport_series and ' ' in child_passport_series:
                    child_passport_series = child_passport_series.replace(' ', '')
                child_passport_number = (
                    user['students_document_number'] if 'Паспорт' in user['students_document'] and user[
                        'students_document_number'] else None)
                child_certificate_series = (
                    user['students_document_series'] if 'Свидетельство' in user['students_document'] else None)
                child_certificate_number = (
                    user['students_document_number'] if 'Свидетельство' in user['students_document'] and user[
                        'students_document_number'] else None)

                parent_passport_series = (
                    user['parent_document_series'] if 'Паспорт' in user['parent_document'] else None)
                if parent_passport_series and ' ' in parent_passport_series:
                    parent_passport_series = parent_passport_series.replace(' ', '')
                parent_passport_number = (
                    user['parent_document_number'] if 'Паспорт' in user['parent_document'] and user[
                        'parent_document_number'] else None)

                if settings.DEBUG:
                    print(user)

                if ParentChild1C.objects.filter(child_UID=user['students_uid']).exists():
                    ParentChild1C.objects.filter(child_UID=user['students_uid']).update(child_surname=child_surname,
                                                                                        parent_surname=parent_surname,
                                                                                        child_name=child_name,
                                                                                        parent_name=parent_name,
                                                                                        child_middle_name=child_middle_name,
                                                                                        parent_middle_name=parent_middle_name,
                                                                                        child_male=child_male,
                                                                                        parent_male=parent_male,
                                                                                        child_birthday=child_birthday,
                                                                                        parent_birthday=parent_birthday,
                                                                                        parent_passport_series=parent_passport_series,
                                                                                        parent_passport_number=parent_passport_number,
                                                                                        parent_phone=parent_phone,
                                                                                        child_passport_series=child_passport_series,
                                                                                        child_passport_number=child_passport_number,
                                                                                        child_certificate_number=child_certificate_number,
                                                                                        child_certificate_series=child_certificate_series)
                else:
                    ParentChild1C.objects.create(child_UID=user['students_uid'],
                                                 parent_UID=user['parent_uid'],
                                                 child_surname=child_surname,
                                                 parent_surname=parent_surname,
                                                 child_name=child_name,
                                                 parent_name=parent_name,
                                                 child_middle_name=child_middle_name,
                                                 parent_middle_name=parent_middle_name,
                                                 child_male=child_male,
                                                 parent_male=parent_male,
                                                 child_birthday=child_birthday,
                                                 parent_birthday=parent_birthday,
                                                 parent_passport_series=parent_passport_series,
                                                 parent_passport_number=parent_passport_number,
                                                 parent_phone=parent_phone,
                                                 child_passport_series=child_passport_series,
                                                 child_passport_number=child_passport_number,
                                                 child_certificate_number=child_certificate_number,
                                                 child_certificate_series=child_certificate_series)

            return Response("OK", status=status.HTTP_200_OK)
        else:
            return Response("Bad login", status=status.HTTP_403_FORBIDDEN)


class ParentChildGetAPIView(APIView):
    """
    Получаем список родители-дети
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request):

        if request.user.is_superuser or Role.objects.filter(staff="ZAV", user=request.user).exists():
            parent_child = ParentChild1C.objects.all()
            serializer = ParentChild1CSerializer(instance=parent_child, many=True)
            data = serializer.data
        else:
            raise serializers.Validation
            Error("permission denied")
        return Response(data, status=status.HTTP_200_OK)


class PartnersAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if request.user.username == '1C':
            users = request.data['partners']

            for user in users:
                surname, name, middle_name, male = clean_FIO(user['partner_name'])
                birthday = get_birthday(user['partner_document_birthDate'])
                phone = (user['partner_phone'] if user['partner_phone'] else None)
                passport_series = (user['partner_document_series'] if 'Паспорт' in user['partner_document'] else None)

                if passport_series and ' ' in passport_series:
                    passport_series = passport_series.replace(' ', '')
                passport_number = (user['partner_document_number'] if 'Паспорт' in user['partner_document'] else None)

                if settings.DEBUG:
                    print(user)

                if Partner1C.objects.filter(UID=user['partner_uid']).exists():
                    Partner1C.objects.filter(UID=user['partner_uid']).update(surname=surname, name=name,
                                                                             middle_name=middle_name, male=male,
                                                                             birthday=birthday, phone=phone,
                                                                             passport_series=passport_series,
                                                                             passport_number=passport_number)
                else:
                    Partner1C.objects.create(UID=user['partner_uid'], surname=surname, name=name,
                                             middle_name=middle_name, male=male, birthday=birthday, phone=phone,
                                             passport_series=passport_series, passport_number=passport_number)

            return Response("OK", status=status.HTTP_200_OK)
        else:
            return Response("Bad login", status=status.HTTP_403_FORBIDDEN)


class PartnersGetAPIView(APIView):
    """
    Получаем список сотрудников
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    def get(self, request):
        if request.user.is_superuser or Role.objects.filter(staff="ZAV", user=request.user).exists():
            partners = Partner1C.objects.all()
            serializer = Partner1CSerializer(instance=partners, many=True)
            data = serializer.data
        else:
            raise serializers.ValidationError("permission denied")
        return Response(data, status=status.HTTP_200_OK)


class SchedulesAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if request.user.username == '1C':
            # with open('schedules.txt', 'w') as f:
            #     for i in request.data['schedules']:
            #         f.write(str(i)+'\n\n')
            # print(request.data)
            return Response("OK", status=status.HTTP_200_OK)
        else:
            return Response("Bad login", status=status.HTTP_403_FORBIDDEN)
