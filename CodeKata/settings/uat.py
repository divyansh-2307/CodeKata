from .base import *

DEBUG = False
ALLOWED_HOSTS = ['uat.example.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codekata',  # UAT database name
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
    }
}