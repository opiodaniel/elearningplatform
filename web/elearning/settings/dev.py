from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Has to be
SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'elearning',
        'USER': 'elearning',
        'PASSWORD': '#123Daniel',
        'HOST': 'localhost',
        'PORT': 5432
    }
}


CURRENT_URL = 'dev'

DOMAIN = 'http://127.0.0.1:8000'
