"""
Django settings for railway project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY', 'default_value')
SECRET_KEY="django-insecure-2f^e6nfs(633kkx-4bc2^n1l8y6d++#=lcx+c@5fzcfiif2n*q"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    # 'django_social_share'
    'rest_framework',
    'corsheaders',
    'oauth2_provider',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # cors resolving middleware

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware', # oauth token middleware
    
]

ROOT_URLCONF = 'railway.urls'

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

WSGI_APPLICATION = 'railway.wsgi.application'

# domain = https://web-production-e388.up.railway.app/

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import dj_database_url

DATABASE_URL = "postgresql://postgres:ZskHB5mEcAusgHxtMMbx@containers-us-west-197.railway.app:6948/railway"

DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
    }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'railway',
#         'USER': 'postgres',
#         'PASSWORD': '1234',
#         'HOST':'localhost',
#         'PORT': '5432',
        
#     }
# }

# from dotenv import load_dotenv

# load_dotenv()
# import os

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DISABLE_COLLECTSTATIC = 0

# CLIENT_ID = "oASmK1HdbaxhecWiO1rrQIB43cLRfNeHuK7Oupix"
# CLIENT_SECRET = "9vbtQWZWtLqdQMb7Rdc0Y06Qqvv4umQW93ORZaJTpZo9ENbB0hFxXjx9FSdCeFFoQsbMS6VI6B30776J0qCbdGzX53P4IxiyyfBc47iQfQp17VdraVewfC4SVvEyRS48"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
   
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
    ],

}
AUTHENTICATION_BACKENDS = [
    # 'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
]


OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 60,
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http','https'],
    'REFRESH_TOKEN_EXPIRE_SECONDS': 300,
    'REQUEST_APPROVAL_PROMPT': 'auto',
    'ROTATE_REFRESH_TOKENS': True,
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    },
}


OAUTH_ACCESS_TOKEN_MODEL = 'oauth2_provider.models.AccessToken'# AUTH_USER_MODEL = 'app.User'

CORS_ORIGIN_ALLOW_ALL = True