from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated

from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer

from main_app.views import IsActive, CustomJWTAuthentication


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Переопределяем класс создания access и refresh токенов с использованием собственного сериализатора
    """
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    """
    Переопределяем класс обновления access и refresh токенов с добавлением авторизации по access токену и с использованием собственного сериализатора
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsActive,)

    serializer_class = MyTokenRefreshSerializer
