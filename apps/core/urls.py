from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.pay, name='pay'),
    path('<str:order_id>/', views.cart_pay, name='cart_pay'),
]
