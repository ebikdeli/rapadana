from .base import *

DEBUG = False

# SECRET_KEY = 'django-insecure-7s4l(vt1vmpatobda4utligb+b)8cxncva4y$al+kf6(i2@b5s'   # WILL CHANGE

# # https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = ['*']   # WILL CHANGE
ALLOWED_HOSTS = ['.rapadana.ir', ]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

MAIN_PORT = 443 if SECURE_SSL_REDIRECT else 80

MAIN_SCHEME = 'https' if SECURE_SSL_REDIRECT else 'http'

PARENT_HOST = 'rapadana.ir'

try:
    from .local import *
except ImportError:
    pass
