from atexit import register
from django.contrib import admin

from .models import Customer, Order, Payment


admin.site.register([Customer, Order, Payment])
