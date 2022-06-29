from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-!b_&88@f!19e#7@as152h5s+k&^424cu3)f#d%&c8bfm-wi!gv'

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False


MAIN_PORT = 8000

MAIN_SCHEME = 'http'

PARENT_HOST = 'localhost'

try:
    from .local import *
except ImportError:
    pass
