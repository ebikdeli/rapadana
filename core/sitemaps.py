"""
https://docs.djangoproject.com/en/4.0/ref/contrib/sitemaps/#django.contrib.sitemaps.Sitemap.location
"""
from django.contrib.sitemaps import Sitemap

# For future use:
# from core.models import Customer, Order


class IndexStaicSitemap(Sitemap):
    """Sitemap updated when when index page changed"""
    changefreq = "monthly"
    priority = 0.4
    location = 'https://rapadana.ir'
    # location = '/'  # If 'location' does not provided, django returns 'get_absolute_url'. Beware of this!

    def items(self):
        # return Customer.objects.none()
        return ['https://rapadana.ir', ]
