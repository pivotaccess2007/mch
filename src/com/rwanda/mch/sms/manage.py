#!/usr/bin/env python
import os
import sys


#activate_this = '/usr/local/venv/rwanda1000/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
