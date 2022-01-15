from .base import *

DEBUG = False

# SECRET_KEY = 'django-insecure-7s4l(vt1vmpatobda4utligb+b)8cxncva4y$al+kf6(i2@b5s'   # WILL CHANGE

ALLOWED_HOSTS = ['*']   # WILL CHANGE

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
