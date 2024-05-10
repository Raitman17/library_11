from pathlib import Path
from dotenv import load_dotenv
from os import getenv, path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'library_app',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'django_minio_backend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'library.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('PG_DBNAME'),
        'USER': getenv('PG_USER'),
        'PASSWORD': getenv('PG_PASSWORD'),
        'HOST': getenv('PG_HOST'),
        'PORT': getenv('PG_PORT'),
        'OPTIONS': {'options': '-c search_path=public,library'},
        'TEST': {
            'NAME': 'test_db',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LOCALE_PATH = 'library_app/locale'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TEST_RUNNER = 'tests.runner.PostgresSchemaRunner'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

if DEBUG:
    AWS_ACCESS_KEY_ID = getenv('MINIO_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = getenv('MINIO_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = getenv('MINIO_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = getenv('MINIO_API')
    AWS_S3_USE_SSL = False

MINIO_ENDPOINT = 'localhost:9000'
MINIO_ACCESS_KEY = getenv('MINIO_ACCESS_KEY_ID')
MINIO_SECRET_KEY = getenv('MINIO_SECRET_ACCESS_KEY')
MINIO_USE_HTTPS = False
MINIO_CONSISTENCY_CHECK_ON_START = bool(getenv('MINIO_CONSISTENCY_CHECK_ON_START', False))
MINIO_PRIVATE_BUCKETS = []
MINIO_PUBLIC_BUCKETS = [
    'static',
]
