from django.urls import path

from .views import ObjectsAPIView, ObjectAPIView, CabinetsAPIView, CabinetAPIView, ClassesAPIView, ClassAPIView, \
    GroupsAPIView, GroupAPIView, LessonsAPIView, LessonAPIView, TimeLessonsAPIView, TimeLessonAPIView, SchedulesAPIView, \
    ScheduleAPIView, StudentClassAPIView, StudentClassesAPIView, StudentGroupAPIView, StudentGroupsAPIView

urlpatterns = [
    path('objects/', ObjectsAPIView.as_view()),
    path('objects/<int:pk>/', ObjectAPIView.as_view()),
    path('cabinets/', CabinetsAPIView.as_view()),
    path('cabinets/<int:pk>/', CabinetAPIView.as_view()),
    path('classes/', ClassesAPIView.as_view()),
    path('classes/<int:pk>/', ClassAPIView.as_view()),
    path('groups/', GroupsAPIView.as_view()),
    path('groups/<int:pk>/', GroupAPIView.as_view()),
    path('lessons/', LessonsAPIView.as_view()),
    path('lessons/<int:pk>/', LessonAPIView.as_view()),
    path('time-lessons/', TimeLessonsAPIView.as_view()),
    path('time-lessons/<int:pk>/', TimeLessonAPIView.as_view()),
    path('schedules/', SchedulesAPIView.as_view()),
    path('schedules/<int:pk>/', ScheduleAPIView.as_view()),
    path('student-classes/', StudentClassesAPIView.as_view()),
    path('student-classes/<int:pk>/', StudentClassAPIView.as_view()),
    path('student-groups/', StudentGroupsAPIView.as_view()),
    path('student-groups/<int:pk>/', StudentGroupAPIView.as_view()),
]
