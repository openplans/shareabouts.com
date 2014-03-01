import os
from django.core.exceptions import ImproperlyConfigured

NOT_SET = object()
def getenv(key, default=NOT_SET):
    if default is NOT_SET:
        try:
            return os.environ[key]
        except KeyError:
            raise ImproperlyConfigured(
                'No environment value for "%s" variable, '
                'and no default value provided.' % (key,))
    else:
        return os.environ.get(key, default)


def loadenv(filename):
    with open(filename) as envfile:
        for line in envfile:
            stripped_line = line.strip()

            # Comment lines
            if stripped_line[0] == '#':
                continue

            # Empty/whitespace lines
            if len(stripped_line) == 0:
                continue

            try:
                key, val = line.split('=', 1)
            except ValueError:
                raise ImproperlyConfigured('Bad line in environment file "%s": "%s"' % (filename, line))

            key = key.strip()
            val = val.strip('\r\n')
            os.environ[key] = val
