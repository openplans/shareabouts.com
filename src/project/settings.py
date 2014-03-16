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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'shareabouts_manager.context_processors.settings',
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
DATABASES = {'default': dj_database_url.config()}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

postgis_version_string = env.get('POSTGIS_VERSION', None)
if postgis_version_string:
    POSTGIS_VERSION = tuple(int(v) for v in postgis_version_string.split('.'))


# ======================================================================
# Cache
# ======================================================================

import django_cache_url
CACHES = {'default': django_cache_url.config()}

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

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Check whether we should use local file system storage (default False) or AWS
uses_local_storage = (env.get('LOCAL_STORAGE', 'False').lower() == 'true')
if uses_local_storage:
    ATTACHMENT_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    # Set up AWS storage
    pass


# ======================================================================
# Django Rest Framework
# ======================================================================

REST_FRAMEWORK = {
    'PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size'
}


# ======================================================================
# Payment Processing
# ======================================================================

STRIPE_SECRET_KEY = env.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = env.get('STRIPE_PUBLIC_KEY')
