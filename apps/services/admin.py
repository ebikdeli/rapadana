from django.contrib import admin

from .models import Category, Service, OrderService


admin.site.register([Category, Service, OrderService])
