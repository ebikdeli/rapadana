from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def index(request):
    data = ['welcome to bigtek. It\'s showing API works properly', {'status_code': 200, 'verify': 'OK'}]
    return JsonResponse(data=data, safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('apis.urls')),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
