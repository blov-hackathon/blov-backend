"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'J$m3KR5MDUWypBQbPsR#psW?W?9cl$1hEq8g3ha3V4HJCH6Jw6&taP!6m6cxK6zEZVjJoM9oX#gNGOnL')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not os.environ.get('PRODUCTION')
PRODUCTION = not DEBUG

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 'localhost, 127.0.0.1').replace(' ', '').split(',')


# Application definition

PRIORITY_APPS = [
    'whitenoise.runserver_nostatic',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'rest_framework',
    'corsheaders',
]

INTERNAL_APPS = [
    'user',
]

INSTALLED_APPS = PRIORITY_APPS + INTERNAL_APPS + EXTERNAL_APPS + DJANGO_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('CUSTOM_DB'):
    import json
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('CUSTOM_DB_ENGINE', 'django.db.backends.mysql'),
            'NAME': os.environ.get('CUSTOM_DB_NAME', 'django'),
            'USER': os.environ.get('CUSTOM_DB_USER', 'django'),
            'PASSWORD': os.environ.get('CUSTOM_DB_PASSWORD', 'django'),
            'HOST': os.environ.get('CUSTOM_DB_HOST', 'db'),
            'PORT': os.environ.get('CUSTOM_DB_PORT', '3306'),
            'OPTIONS': json.loads(os.environ.get('CUSTOM_DB_OPTIONS', '{\'chartset\':\'utf8mb4\'}')),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework Config
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "config.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# CORS Control
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8080',
    'http://125.133.60.213',
)

# AWS Config
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Celery Config
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60

# Email Config (AWS SES)
# EMAIL_BACKEND = 'django_ses.SESBackend'
# DEFAULT_FROM_EMAIL = os.environ.get(
#     'EMAIL_FROM_ADDR', 'no-reply <no-reply@nobody')
# AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME', 'ap-northeast-2')
# AWS_SES_REGION_ENDPOINT = os.environ.get(
#     'AWS_SES_REGION_ENDPOINT', f'email.{AWS_SES_REGION_NAME}.amazonaws.com')
# AWS_SES_ACCESS_KEY_ID = os.environ.get(
#     'AWS_SES_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID)
# AWS_SES_SECRET_ACCESS_KEY = os.environ.get(
#     'AWS_SES_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY)

# Security Settings
# SECURE_SSL_REDIRECT = PRODUCTION
# SECURE_HSTS_SECONDS = None if not PRODUCTION else 60 * 60 * 24 * 365
# SECURE_HSTS_PRELOAD = PRODUCTION
# SECURE_HSTS_INCLUDE_SUBDOMAINS = PRODUCTION
# SESSION_COOKIE_SECURE = PRODUCTION
# CSRF_COOKIE_SECURE = PRODUCTION

# Custom User Model
AUTH_USER_MODEL = 'user.User'
