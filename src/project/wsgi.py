"""
WSGI config for the project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(REPO_DIR, 'lib', 'api', 'src'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from dj_static import Cling
application = Cling(application)

from .gzip_middleware import GzipMiddleware
application = GzipMiddleware(application)

from .twinkie import ExpiresMiddleware
application = ExpiresMiddleware(application, {
    'application/javascript': 365*24*60*60,
    'text/css':               365*24*60*60,
    'image/png':              365*24*60*60,
})
