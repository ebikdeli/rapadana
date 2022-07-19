from django.urls import path

from . import views


app_name = 'services'

urlpatterns = [
    path(route='', view=views.service_index, name='service_index')
]
