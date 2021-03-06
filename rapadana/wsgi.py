"""
WSGI config for rapadana project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# For development
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rapadana.settings.dev')
# For production
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rapadana.settings.production')
application = get_wsgi_application()
