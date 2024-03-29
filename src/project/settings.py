"""
Django settings for the project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from project.env_utils import Environment
env = Environment(os.environ)

# Load the local environment file if one is available
try:
    envfile = open(os.path.join(BASE_DIR, 'local.env'))
except IOError:
    pass
else:
    try: env.load(envfile)
    finally: envfile.close()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# ======================================================================
# Access, security, and cryptography
# ======================================================================

SECRET_KEY = env.get('SECRET_KEY')
ALLOWED_HOSTS = env.get('ALLOWED_HOSTS').split(',')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
HTTPS_ENABLED = (env.get('HTTPS', 'off').lower() in ('true', 'yes', 'on'))


# ======================================================================
# Troubleshooting and debugging
# ======================================================================

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (env.get('DEBUG', 'False').lower() == 'true')
TEMPLATE_DEBUG = DEBUG or (env.get('TEMPLATE_DEBUG', 'False').lower() == 'true')

INTERNAL_IPS = ('127.0.0.1',)


# ======================================================================
# Application definition
# ======================================================================

INSTALLED_APPS = (
    # Project apps
    'sa_api',
    'sa_api_v2',
    'sa_api_v2.apikey',
    'sa_api_v2.cors',
    'shareabouts_manager',

    # 3rd-party apps
    'jstemplate',
    'djangobars',
    'rest_framework',
    'south',
    'social.apps.django_app.default',

    # Core/contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)

HANDLEBARS_APP_DIRNAMES = ['jstemplates']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

LOGIN_URL = 'manager-signin'
LOGOUT_URL = 'manager-index'

WSGI_APPLICATION = 'project.wsgi.application'


# ======================================================================
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# ======================================================================

import dj_database_url
DATABASES = {'default': dj_database_url.config(default=env.get('DATABASE_URL'))}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# ======================================================================
# Cache
# ======================================================================

import django_cache_url
CACHES = {'default': django_cache_url.config(default=env.get('CACHE_URL'))}

# How long to keep api cache values. Since the api will invalidate the cache
# automatically when appropriate, this can (and should) be set to something
# large.
API_CACHE_TIMEOUT = 604800  # a week


# ======================================================================
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
# ======================================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ======================================================================
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# ======================================================================

# Check whether we should use local file system storage (default False) or AWS
uses_local_storage = (env.get('LOCAL_STORAGE', 'False').lower() == 'true')
if uses_local_storage:
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    ATTACHMENT_STORAGE = 'django.core.files.storage.FileSystemStorage'

else:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = env.get('SHAREABOUTS_AWS_KEY')
    AWS_SECRET_ACCESS_KEY = env.get('SHAREABOUTS_AWS_SECRET')
    AWS_STORAGE_BUCKET_NAME = env.get('SHAREABOUTS_AWS_BUCKET')
    AWS_QUERYSTRING_AUTH = False
    AWS_PRELOAD_METADATA = True

    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
    STATIC_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

    ATTACHMENT_STORAGE = DEFAULT_FILE_STORAGE


# ======================================================================
# Django Rest Framework
# ======================================================================

REST_FRAMEWORK = {
    'PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size'
}
