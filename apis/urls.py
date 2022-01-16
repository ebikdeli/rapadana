from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from core import views as core_views


app_name = 'api'

router = DefaultRouter()
router.register('customers', views.CustomerViewSet, 'customer')
router.register('order', views.OrderViewSet, 'order')

urlpatterns = [
    path('', include(router.urls)),
    path('pay/', core_views.pay, name='pay'),
    path('pay/cart/', core_views.cart_pay, name='cart_pay')
]
