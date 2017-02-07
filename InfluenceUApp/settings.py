"""
Django settings for InfluenceUApp.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$6(x*g_2g9l_*g8peb-@anl5^*8q!1w)k&e&2!i)t6$s8kia95'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

# Application definition

INSTALLED_APPS = (
    "sslserver",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosecure',
    'rest_framework',
    'compressor',
    'verification',
    'django.contrib.sites',
    'django_twilio',
    'simple_email_confirmation',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'csp.middleware.CSPMiddleware',
)

ROOT_URLCONF = 'InfluenceUApp.urls'

WSGI_APPLICATION = 'InfluenceUApp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

import dj_database_url

# Right now being used for testing purposes
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# change to true when in production!!!
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request'
            ],
        },
    },
]

REST_FRAMEWORK = {
    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'luxahrlite@gmail.com'
EMAIL_HOST_PASSWORD = 'BixbyMontreal1995'
EMAIL_PORT = 587
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Security
SECURE_FRAME_DENY = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
#
# CSP_DEFAULT_SRC = "'self'"
# CSP_SCRIPT_SRC = ("'self'", 'https://127.0.0.1:8000/', "'unsafe-inline'", 'code.jquery.com', 'www.google-analytics.com', 'cdnjs.cloudflare.com',
#                   'maxcdn.bootstrapcdn.com')
# CSP_IMG_SRC = ("'self'", 'www.google-analytics.com', 'https://cdnjs.cloudflare.com')
# CSP_MEDIA_SRC = ("'self'", 'https://static.olark.com')
# CSP_FONT_SRC = ("'self'", 'cdn.comfonts.googleapis.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com',
#                 'maxcdn.bootstrapcdn.com')
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", 'maxcdn.bootstrapcdn.com', 'cdnjs.cloudflare.com', 'fonts.googleapis.com')
# CSP_CONNECT_SRC = "'self'"
# CSP_CHILD_SRC = "'self'"

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True


#TWILIO
TWILIO_ACCOUNT_SID = "ACe566714112033a0e33e96148f8c6dc02"
TWILIO_AUTH_TOKEN = "d1e0f2b919245b1f13a490340e69b126"
TWILIO_DEFAULT_CALLERID = 'InfluenceU'


#EMAIL VERIFICATION
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_OPEN = True
