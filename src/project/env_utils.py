from django.core.exceptions import ImproperlyConfigured

NOT_SET = object()


class Environment:
    def __init__(self, envvars=None):
        self.vars = envvars or {}

    def get(self, key, default=NOT_SET):
        if default is NOT_SET:
            try:
                return self.vars[key]
            except KeyError:
                raise ImproperlyConfigured(
                    'No environment value for "%s" variable, '
                    'and no default value provided.' % (key,))
        else:
            return self.vars.get(key, default)

    def load(self, envfile, clean=False):
        if clean: self.vars = {}

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
                raise ImproperlyConfigured('Bad line in environment file "%s": "%s"' % (envfile.name, line))

            key = key.strip()
            val = val.strip('\r\n')
            self.vars[key] = val