"""
https://docs.djangoproject.com/en/4.0/ref/contrib/sitemaps/#django.contrib.sitemaps.Sitemap.location
"""
from django.contrib.sitemaps import Sitemap

# For future use:
# from core.models import Customer, Order


class CustomerSitemap(Sitemap):
    """Sitemap updated when every new customer added or updated in database"""
    changefreq = "weekly"
    priority = 0.4
    location = 'https://rapadana.ir'
    # location = '/'  # If 'location' does not provided, django returns 'get_absolute_url'. Beware of this!

    def items(self):
        # return Customer.objects.none()
        return ['https://rapadana.ir', ]


class OrderSitemap(Sitemap):
    """Sitemap updated when every new order added or modified to database"""
    changefreq = 'weekly'
    priority = 0.4
    location = 'https://rapadana.ir'

    def items(self):
        # return Order.objects.none()
        return ['https://rapadana.ir', ]
