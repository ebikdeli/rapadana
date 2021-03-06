from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from apps.core import views as core_views


app_name = 'api'

router = DefaultRouter()
router.register('customers', views.CustomerViewSet, 'customer')
router.register('order', views.OrderViewSet, 'order')
router.register('user', views.UserViewSet, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('pay/', core_views.pay, name='pay'),
    path('pay/cart/<str:order_id>/', core_views.cart_pay, name='cart_pay'),
    path('customer-request/', views.CustomerRequest.as_view()),
]
