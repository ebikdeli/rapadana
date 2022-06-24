from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Blog, Comment, File
from .forms import BlogModelForm


class FileAdminInline(ct_admin.GenericTabularInline):
    model = File


class CommentAdminInline(ct_admin.GenericStackedInline):
    model = Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [FileAdminInline, CommentAdminInline]
    form = BlogModelForm


admin.register([Comment, File])
