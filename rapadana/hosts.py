"""
https://django-hosts.readthedocs.io/en/latest/
"""

from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    # These are examples:
    host(r'(|www)', settings.ROOT_URLCONF, name='www'),
    host('blog', 'blog.urls', name='blog'),
)
