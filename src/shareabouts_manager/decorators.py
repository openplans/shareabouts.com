"""
ssl_required decorator
----------------------
Redirect requests to the given to to HTTPS if they are not secure already.
Source: https://djangosnippets.org/snippets/1351/
Author: pjs (https://djangosnippets.org/users/pjs/)
"""

try:
    # Python 2
    import urlparse
except ImportError:
    # Python 3
    from urllib import parse as urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


def ssl_required(view_func):
    def is_ssl_enabled(request):
        # If explicitly off, then it's off
        if not getattr(settings, 'HTTPS_ENABLED', True):
            return False

        # If you're debugging and coming from an internal IP address, it's off
        elif settings.DEBUG and request.META.get('REMOTE_ADDR', None) in settings.INTERNAL_IPS:
            return False

        # Otherwise, it's on
        else:
            return True

    def _checkssl(request, *args, **kwargs):
        if is_ssl_enabled(request) and not request.is_secure():
            if hasattr(settings, 'SSL_DOMAIN'):
                url_str = urlparse.urljoin(
                    settings.SSL_DOMAIN,
                    request.get_full_path()
                )
            else:
                url_str = request.build_absolute_uri()
            url_str = url_str.replace('http://', 'https://', 1)
            return HttpResponsePermanentRedirect(url_str)

        return view_func(request, *args, **kwargs)
    return _checkssl
