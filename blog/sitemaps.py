from django.contrib.sitemaps import Sitemap
from blog.models import Blog

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Blog.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated
