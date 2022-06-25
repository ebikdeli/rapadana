"""
https://django-hosts.readthedocs.io/en/latest/
"""

from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    # These are examples:
    host(r'blog', 'blog.urls', name='blog'),
    host(r'(|www)', settings.ROOT_URLCONF, name='www'),
)
