from django.urls import path

from . import views


app_name = 'services'

urlpatterns = [
    path(route='', view=views.service_index, name='index'),
    path('select/', views.service_select, name='select'),
    path('order/', views.service_order, name='order'),
    path('verify/', views.service_order_verify, name='order_verify'),
]
