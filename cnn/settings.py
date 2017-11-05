"""
Django settings for cnn project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nelm=lt5py*dcarm7$o9k_aetvcff0$sb@sl$#ww4)jw^+_!51'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['python-cnn.herokuapp.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'litecnn',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'cnn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cnn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )


STATIC_ROOT =  os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "staticfiles")

MEDIA_ROOT =  os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media")


AWS_REGION = os.environ.get('AWS_REGION', '')  # e.g. eu-west-1  
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET', '')
AWS_S3_CALLING_FORMAT = "boto.s3.connection.OrdinaryCallingFormat"
AWS_PRELOAD_METADATA = True


if AWS_STORAGE_BUCKET_NAME:
    STATIC_URL = 'https://s3-%s.amazonaws.com/%s/static/' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
    MEDIA_URL = 'https://s3-%s.amazonaws.com/%s/media/' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
    STATICFILES_STORAGE = 'cnn.customstorages.StaticStorage'
    DEFAULT_FILE_STORAGE = 'cnn.customstorages.MediaStorage'
    STATICFILES_LOCATION = 'static'  # name of folder within bucket
    MEDIAFILES_LOCATION = 'media'    # name of folder within bucket
    SECURE_SSL_REDIRECT = True
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'


MEDIA_URL = os.environ.get('MEDIA_URL', MEDIA_URL)
STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)


def get_static_memcache():
    # For python 2.7, just 'import urlparse'
    from urllib.parse import urlparse

    if os.environ.get('REDIS_URL', ''):
        redis_url = urlparse(os.environ.get('REDIS_URL'))
        return {
            "BACKEND": "redis_cache.RedisCache",
            'TIMEOUT': None,
            "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
            "OPTIONS": {
                "PASSWORD": redis_url.password,
                "DB": 0,
            }
        }
    return {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': None,
        'OPTIONS': {
            'MAX_ENTRIES': 5000
        }
    }

CACHES = {
    # Replace the default cache with your existing one (if you have any)
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    },
    'collectfast': get_static_memcache(),
}

COLLECTFAST_CACHE = 'collectfast'


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'