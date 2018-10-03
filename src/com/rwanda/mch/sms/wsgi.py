"""
WSGI config for rapidsmsrw1000 project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
#print "WE ARE THERE"
# set up python path and virtualenv
#activate_this = '/home/aidspan/projects/python/livemas/mch/rwanda/bin/activate_this.py'
activate_this = '/livemas/mch/rwanda/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

filedir = os.path.dirname(__file__)

rootpath = os.path.join(filedir, '')
sys.path.append(os.path.join(rootpath))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")


# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
from celery import Celery

app = Celery('sms')

application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
