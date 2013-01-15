===========
O2W django Utilities
===========

This repository pretend to be in a near future a bunch of useful
utilities and apps for developing using Djando Framework.

How to install
==============

git clone https://github.com/josesanch/o2w_django.git o2w


Add to your INSTALLED_APPS any of the applications

* o2w.admin:
-----------
Visual Enhancements for django admin

* o2w.settings
-------------
Common settings to be used in your projects.

In your common.py
________________

::
#encoding:utf-8
import sys
from os.path import abspath, dirname, join, normpath
######### PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Add all necessary filesystem paths to our system path so that we can use
# python import statements.
sys.path.append(dirname(DJANGO_ROOT))
sys.path.append(normpath(join(DJANGO_ROOT, '../apps')))
sys.path.append(normpath(join(DJANGO_ROOT, '../libs')))
########## END PATH CONFIGURATION

import o2w.settings
o2w.settings.DJANGO_ROOT = DJANGO_ROOT
from o2w.settings.common import *

In your dev.py
________________
from common import *
from o2w.settings.dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}



MIDDLEWARE_CLASSES += EXTRA_MIDDLEWARE_CLASSES
INSTALLED_APPS += EXTRA_INSTALLED_APPS



In your prod.py
________________
from common import *
from o2w.settings.prod import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}



MIDDLEWARE_CLASSES += EXTRA_MIDDLEWARE_CLASSES
INSTALLED_APPS += EXTRA_INSTALLED_APPS




* o2w.comments
-------------

* o2w.users
-------------
* o2w.social
-------------
* o2w.shop
-------------
* o2w.users
-------------
* o2w.contactform
-------------
