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
from filebrowser.sites import site

from core.sitemaps import CustomerSitemap, OrderSitemap


def index(request):
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
sitemaps = {'customer': CustomerSitemap, 'order': OrderSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('apis.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
    path('', index, name='index'),
    path('re', redirect_header)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
