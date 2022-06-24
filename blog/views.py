from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Blog


def some_blog(request):
    return HttpResponse("<h1>Subdomain blog just works!</h1>")

class BlogListView(ListView):
    """Everyone can see all blogs"""
    template_name = 'blog/templates/blog/blog_list_view.html'
    model = Blog
    context_object_name = 'blogs'


class BlogDetalView(DetailView):
    """Everyone can every blog with detail"""


class BlogCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Only authorized users can create new blog"""
