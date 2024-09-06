from django.urls import path

from .views import MyTokenRefreshView, MyTokenObtainPairView

urlpatterns = [
    path('create/', MyTokenObtainPairView.as_view(), name='token_create'),
    path('refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
