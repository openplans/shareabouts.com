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
    'rest_framework',
    'south',

    # Core/contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


# ======================================================================
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# ======================================================================

import dj_database_url
DATABASES = {'default': dj_database_url.config()}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


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
