from django.urls import path

from .views import DirectorsAPIView, DirectorAPIView, TeachersAPIView, TeacherAPIView, FacultativeTeachersAPIView, \
    FacultativeTeacherAPIView, TutorsAPIView, TutorAPIView, ParentsAPIView, ParentAPIView, StudentsAPIView, \
    StudentAPIView, FoodsAPIView, FoodAPIView, ParentChildsAPIView, ParentChildAPIView

urlpatterns = [
    path('directors/', DirectorsAPIView.as_view()),
    path('directors/<int:pk>/', DirectorAPIView.as_view()),
    path('teachers/', TeachersAPIView.as_view()),
    path('teachers/<int:pk>/', TeacherAPIView.as_view()),
    path('facultative-teachers/', FacultativeTeachersAPIView.as_view()),
    path('facultative-teachers/<int:pk>/', FacultativeTeacherAPIView.as_view()),
    path('tutors/', TutorsAPIView.as_view()),
    path('tutors/<int:pk>/', TutorAPIView.as_view()),
    path('parents/', ParentsAPIView.as_view()),
    path('parents/<int:pk>/', ParentAPIView.as_view()),
    path('students/', StudentsAPIView.as_view()),
    path('students/<int:pk>/', StudentAPIView.as_view()),
    path('foods/', FoodsAPIView.as_view()),
    path('foods/<int:pk>/', FoodAPIView.as_view()),
    path('parent-child/', ParentChildsAPIView.as_view()),
    path('parent-child/<int:pk>/', ParentChildAPIView.as_view()),
]
