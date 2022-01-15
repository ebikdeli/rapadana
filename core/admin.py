from atexit import register
from django.contrib import admin

from .models import Order


admin.site.register(Order)
