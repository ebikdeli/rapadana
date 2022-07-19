"""
In this module we implemented two views to show how HttpResponse instances functions and how we can add
arbitrary headers to our responses to client.
"""
from django.contrib import admin
from django.urls import path, include, reverse
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.sitemaps.views import sitemap

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
# from two_factor.urls import urlpatterns as tf_urls

from apps.core.sitemaps import IndexStaicSitemap


def index(request):
    from constance import config
    print('"constance" discount percent: ', config.discount)
    data = ['welcome to bigtek. It\'s showing API works properly', {'status_code': 200, 'verify': 'OK'}]
    response = JsonResponse(data=data, safe=False)

    head = {'name': 'ehsan', 'age': 30}
    for k, v in head.items():
        response.headers[k] = v

    return response
    # return JsonResponse(data=data, safe=False)


def redirect_header(request):
    """This simple view show us how to return data to client with headers"""
    head = {'name': 'ehsan', 'age': 30}
    re = redirect(reverse('index'))
    for k, v in head.items():
        re.headers[k] = v
    re.headers['data_set'] = {'data': 'This is data', 'li': ['data is jsonable', 'good', 25]}
    re.headers['persian'] = 'چرا inchenin ast'
    return re

# This is for import sitemaps:
sitemaps = {'index_sitemap': IndexStaicSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),

    path("__reload__/", include("django_browser_reload.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
    path('watchman/', include('watchman.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),

    path('blog/', include('apps.blog.urls')),
    path('core/', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('api/', include('apps.apis.urls')),

    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
    
    path('', index, name='index'),
    path('re', redirect_header)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
