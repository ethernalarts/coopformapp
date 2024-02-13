"""
Django settings for coopformapp project.
Generated by 'django-admin startproject' using Django 4.0.6.
"""

import dj_database_url
import environ
import os


env = environ.Env()
environ.Env.read_env()


# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
# EMAIL_USE_SSL = env('EMAIL_USE_SSL')
RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')

ADMIN_USERNAME = env('ADMIN_USERNAME')
ADMIN_EMAIL = env('ADMIN_EMAIL')
ADMIN_PASSWORD = env('ADMIN_PASSWORD')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')


ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'form.apps.FormConfig',
    'django_cleanup.apps.CleanupConfig',
    'tailwind',
    'theme',
    'django_browser_reload',
    'widget_tweaks',
    'active_link',
    'phonenumber_field',
    'django_htmx',
    'wkhtmltopdf',
    'rest_framework',
    'api',
]

TAILWIND_APP_NAME = 'theme'
TAILWIND_CSS_PATH = 'css/dist/styles.css'
INTERNAL_IPS = [
    "127.0.0.1",
]

# Django Active Link
ACTIVE_LINK_CSS_CLASS = 'active'
ACTIVE_LINK_STRICT = 'False'

NPM_BIN_PATH = r"C:/Program Files/nodejs/npm.cmd"

WKHTMLTOPDF_BIN = "C:/Program Files/wkhtmltopdf/bin/ ./manage.py runserver"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'coopformapp.urls'

CSRF_FAILURE_VIEW = 'form.views.csrf_failure'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
APPEND_SLASH = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Location of static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Location of media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


FORM_STATIC = os.path.join(BASE_DIR, "form/templates/static/")
THEME_STATIC = os.path.join(BASE_DIR, "theme/static/")
STATICFILES_DIRS = [ FORM_STATIC, THEME_STATIC ]


# Template Directories
ROOT = os.path.join(BASE_DIR, 'templates')
FORM = os.path.join(BASE_DIR, 'form/templates/')
THEME = os.path.join(BASE_DIR, 'theme/templates/')
API = os.path.join(BASE_DIR, 'api/templates/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ ROOT, FORM, THEME ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'coopformapp.wsgi.application'

# WKHTMLTOPDF_CMD = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(
        env('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    ),
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


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [('en', 'English')]
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True


# Phone Number
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'NG'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'


# REST FRAMEWORK
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%a, %b %d, %Y, %I:%M %p",

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,

    'DEFAULT_PARSER_CLASSES': (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ),
}
