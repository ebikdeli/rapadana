from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from sorl.thumbnail.admin import AdminImageMixin

from .models import User


class UserAdmin(AdminImageMixin, BaseUserAdmin):
    list_display = ('username', 'email', 'phone', 'address', 'is_superuser')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'address', 'name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser')}),
        ('Pictures', {'fields': ('picture', 'background')}),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register([Group, Permission])
