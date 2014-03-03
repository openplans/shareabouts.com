#!/usr/bin/env python
import os
import sys

REPO_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(REPO_DIR, 'lib', 'api', 'src'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
