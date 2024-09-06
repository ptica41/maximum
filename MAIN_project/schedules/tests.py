from django.core.management.base import BaseCommand
from schedules.models import Schedule
from random import randint


for i in range(24000):
    name = f'Запись {i}'
    value = randint(1, 100)
    Schedule.objects.create(date='2024-11-11T00:00:00+03:00', number=1, lesson_id=1, cls_id=1, cabinet_id=1, time_lesson_id=2)