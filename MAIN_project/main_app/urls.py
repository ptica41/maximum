from django.urls import path

from .views import WhoAmIView, SchoolDBAPIView, SchoolsDBAPIView, UploadPhotoAPIView, \
    PhotoAPIView, PhotoMinAPIView, MyChildrenAPIView, UsersAPIView, UserAPIView, \
    SchoolDirectorsAPIView, SchoolTeachersAPIView, SchoolFacultativeTeachersAPIView, SchoolTutorsAPIView, \
    SchoolParentsAPIView, SchoolStudentsAPIView, SchoolFoodsAPIView, UserRolesAPIView, SchoolParentChildAPIView

urlpatterns = [
    path('whoami/', WhoAmIView.as_view()),
    path('my-children/', MyChildrenAPIView.as_view()),
    path('users/<int:pk>/', UserAPIView.as_view()),
    path('users/<int:pk>/roles/', UserRolesAPIView.as_view()),
    path('users/', UsersAPIView.as_view()),
    path('schools/', SchoolsDBAPIView.as_view()),
    path('schools/<int:pk>/', SchoolDBAPIView.as_view()),
    path('schools/<int:pk>/directors/', SchoolDirectorsAPIView.as_view()),
    path('schools/<int:pk>/teachers/', SchoolTeachersAPIView.as_view()),
    path('schools/<int:pk>/facultative-teachers/', SchoolFacultativeTeachersAPIView.as_view()),
    path('schools/<int:pk>/tutors/', SchoolTutorsAPIView.as_view()),
    path('schools/<int:pk>/parents/', SchoolParentsAPIView.as_view()),
    path('schools/<int:pk>/students/', SchoolStudentsAPIView.as_view()),
    path('schools/<int:pk>/foods/', SchoolFoodsAPIView.as_view()),
    path('schools/<int:pk>/parent-child/', SchoolParentChildAPIView.as_view()),
    path('photo/', UploadPhotoAPIView.as_view()),
    path('photo/<int:pk>/', PhotoAPIView.as_view()),
    path('photo-min/<int:pk>/', PhotoMinAPIView.as_view()),
]
