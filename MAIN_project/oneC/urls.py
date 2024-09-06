from django.urls import path

from .views import ParentChildAPIView, PartnersAPIView, PartnersGetAPIView, ParentChildGetAPIView, SchedulesAPIView


urlpatterns = [
    path('users/', ParentChildAPIView.as_view()),
    path('users-get/', ParentChildGetAPIView.as_view()),
    path('partners/', PartnersAPIView.as_view()),
    path('partners-get/', PartnersGetAPIView.as_view()),
    path('schedules/', SchedulesAPIView.as_view()),
]
