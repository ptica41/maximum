from pathlib import Path
import os

from dotenv import load_dotenv  # библиотека для загрузки переменных окружения
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# расположение файла переменных окружения
dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')

# загружаем переменные окружения
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv('DEBUG', default=0))

# Список разрешенных хостов
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(' ')

# Указываем модули проекта
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main_app.apps.MainAppConfig',
    'token_app.apps.TokenAppConfig',
    'oneC.apps.OnecConfig',
    'roles.apps.RolesConfig',
    'schedules.apps.SchedulesConfig',

    'django_filters',
    'phonenumber_field',  # для валидации поля phone в моделях
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_swagger',
]

# Настройка REST API
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated', ],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication', ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter',
                                'rest_framework.filters.OrderingFilter'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

# Настройка токенов авторизации
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),  # в swagger'e указываем в security "bearerAuth"
}

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # добавляем для CORS запросов
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# указываем расположение файла с роутами
ROOT_URLCONF = 'MAIN_project.urls'

# шаблоны веб-страниц по умолчанию (в этом проекте не используется)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
]

WSGI_APPLICATION = 'MAIN_project.wsgi.application'

# настройка БД микросервиса
DATABASES = {
    'default': {
        'ENGINE': os.getenv("SQL_ENGINE"),
        'NAME': os.getenv("SQL_DATABASE"),
        'USER': os.getenv("SQL_USER"),
        'PASSWORD': os.getenv("SQL_PASSWORD"),
        'HOST': os.getenv("SQL_HOST"),
        'PORT': os.getenv("SQL_PORT")
    }
}

# явно указываем пользовательскую модель
AUTH_USER_MODEL = 'main_app.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# настройка паролей пользователя по умолчанию
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# # инициализация ключа шифрования паролей для БД школ
# PASSWORD_SCHOOL = os.getenv("PASSWORD_SCHOOL")

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

# указываем регион для библиотеки phonenumbers (используется в поле phone модели users)
PHONENUMBER_DEFAULT_REGION = 'RU'

# указываем часовой пояс сервера прода для корректной записи в БД
TIME_ZONE = os.getenv("TIME_ZONE")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static_root'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    # '/var/www/static/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# указываем хосты для CORS поддержки (для фронта)
# CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS").split(" ")
CORS_ORIGIN_ALLOW_ALL = True

# настраиваем swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}
