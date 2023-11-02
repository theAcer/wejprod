"""
Django settings for azureproject project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

if 'CODESPACE_NAME' in os.environ:
    CODESPACE_NAME = os.getenv('CODESPACE_NAME')
    GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN = os.getenv('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')
    
    # Create the trusted origin for the CodeSpace
    codespace_origin = f'https://{CODESPACE_NAME}-8000.{GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}'
    
    # Add localhost to the trusted origins
    CSRF_TRUSTED_ORIGINS = [codespace_origin, 'https://localhost:8000']
else:
    # Set trusted origins to only include localhost if CODESPACE_NAME is not in the environment
    CSRF_TRUSTED_ORIGINS = ['https://localhost:8000/', 'https://127.0.0.1:8000/']

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'apps.firebase_auth',
    'restaurant_review.apps.RestaurantReviewConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'django_extensions',
    'silk',
    'rest_framework_swagger',
    
    

    #local
    'apps.users.apps.UsersConfig', 
    'apps.dashboard.apps.DashboardConfig',
    'apps.courses',
    'apps.games',
    'apps.tournaments',
    'apps.party',
    'apps.friendship',
    'apps.wagers',
    'apps.chat',


     #thirdparty
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'bootstrap_datepicker_plus',
    'debug_toolbar',
    'drf_yasg',
    'channels',
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '727074524293-sk1e4vqi9jlme9o57gt0vg1e2ms9q1q8.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

#django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

LOGIN_REDIRECT_URL ='home'
ACCOUNT_LOGOUT_REDIRECT = 'home'

#django-allauth config
SITE_ID = 1

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'firebase_auth.authentication.FirebaseAuthentication',
)

AUTH_USER_MODEL = 'users.CustomUser'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_FROM_EMAIL = 'samsonnjogu@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.AllowAny'
        ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],

}
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
CORS_ALLOW_CREDENTIALS = True  # You may need this depending on your setup
CORS_ORIGIN_WHITELIST = (
    'https://localhost:8000',
)
CORS_ORIGIN_ALLOW_ALL = True 

ROOT_URLCONF = 'azureproject.urls'

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
ASGI_APPLICATION = 'azureproject.asgi.application'
#WSGI_APPLICATION = 'azureproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# To use sqllite as the database engine,
#   uncomment the following block and comment out the Postgres section below

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }


# Configure Postgres database for local development
#   Set these environment variables in the .env file for this project.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME'),
        'HOST': os.environ.get('DBHOST'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

#MEDIA 
MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATE_FORMAT = "d/m/Y"
USE_L10N = False

# Add the apps directory to the sys.path
sys.path.append(os.path.join(BASE_DIR, 'apps'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

FIREBASE_CONFIG = {
  "apiKey": "AIzaSyBlIjlgcWQxRoSbt0GJpe-hBfEJKdAaptw",
  "authDomain": "wejja-78a11.firebaseapp.com",
  "databaseURL": "https://wejja-78a11-default-rtdb.firebaseio.com",
  "projectId": "wejja-78a11",
  "storageBucket": "wejja-78a11.appspot.com",
  "messagingSenderId": "762433816574",
  "appId": "1:762433816574:web:6b06c7a890ff68ffff22af",
  "measurementId": "G-B3FWHHBFDN"
}