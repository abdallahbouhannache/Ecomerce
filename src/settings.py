"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from src.ckeditor import CKEDITOR_CONFIGS
# import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
# seetheroot123
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Satim
# SATIM_USERNAME = "SAT2104130142"
# SATIM_PASSWORD = "satim120"
# SATIM_ID       = "E010900123"
SATIM_USERNAME = config('SATIM_USERNAME')
SATIM_PASSWORD = config('SATIM_PASSWORD')
SATIM_ID       = config('SATIM_ID')

# SATIM API Endpoints
SATIM_CREATE_API = config('SATIM_CREATE_API')
SATIM_CONFIRM_API = config('SATIM_CONFIRM_API')
SATIM_REFUND_API = config('SATIM_REFUND_API')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", cast=bool)

DEBUG = False

HTTP_PROTOCOL = config("HTTP_PROTOCOL") # http local and https in production
HTTP_HOST = config("HTTP_HOST") # 127.0.0.1:8000 local and www.elamanecc.com.dz in production


ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd Party Apps
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
    'django_recaptcha',
    'maintenance_mode',
    # My Apps
    'home',
    'membership',
    'page',
    'store',
    'shipping',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_proccessor.view_cart',
                'home.context_proccessor.view_carousel',
                'home.context_proccessor.view_category',
                'maintenance_mode.context_processors.maintenance_mode',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases



# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL'),
#         conn_max_age=600,
#         ssl_require=True
#     )
# }

# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
# }


# DATABASES = {
#     'default': dj_database_url.config(default='mysql://u287902405_root:vpsPass@1375@srv1471.hstgr.io:3306/u287902405_djangodb')
# }
    

# main-hosting.com

# default='mysql://u287902405_root:vpsPass@1375@u287902405_djangodb.main-hosting.com:3306/u287902405_djangodb'

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
# }

# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get(str(BASE_DIR / 'db.sqlite3')),
#         conn_max_age=600,
#         ssl_require=True
#     )
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
# else:
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASS'),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'your_database_name',
    #     'USER': 'your_database_user',
    #     'PASSWORD': 'your_database_password',
    #     'HOST': 'mysql.hostinger.com',  # Replace with your Hostinger MySQL server's hostname
    #     'PORT': '3306',
    # }
# }

# Shipping DB
SHIPPING_SCHEMA = BASE_DIR / "shipping/db/schema.json"
SHIPPING_DB = BASE_DIR / "shipping/db/database.json"
WILAYA = BASE_DIR / "shipping/db/wilaya.json"
COMMUNES = BASE_DIR / "shipping/db/communes.json"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Algiers'

USE_I18N = True

LANGUAGES = [
    ['en', "English"],
    ['ar', "العربية"],
    ['fr', "French"],
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

USE_L10N = True

USE_TZ = True

# SELENIUM_DRIVER = BASE_DIR / 'src/chromedriver'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = f'{BASE_DIR}{STATIC_URL}'
STATICFILES_URL = '/staticfiles/'
STATICFILES_DIRS = [f'{BASE_DIR}{STATICFILES_URL}',]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media 
MEDIA_URL = '/media/'
MEDIA_ROOT =  f'{BASE_DIR}{MEDIA_URL}'


# Email
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Email
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = config('ADMIN_EMAIL')


# Error tracking

# Error tracking
ADMINS = [
    tuple(admin.split(',')) for admin in config('ADMINS').split(';')
]


# Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = '/'


# Ckeditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',]},
            {'name': 'links', 'items': ['Link', 'Unlink',]},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            '/',  # put this to force next toolbar on new line,
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'width': '100%',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}


RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_SITE_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_SECRET_KEY')


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


MAINTENANCE_MODE_STATE_FILE_PATH = 'emergency.txt'
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
