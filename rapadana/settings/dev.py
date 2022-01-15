from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-!b_&88@f!19e#7@as152h5s+k&^424cu3)f#d%&c8bfm-wi!gv'

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
