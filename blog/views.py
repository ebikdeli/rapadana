from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, DetailView, CreateView,\
    UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse as rev
from django_hosts.resolvers import reverse_lazy, reverse, reverse_host

from .models import Blog
from .forms import BlogModelForm


def some_blog(request):
    return HttpResponse("<h1>Subdomain blog just works!</h1>")

class BlogListView(ListView):
    """Everyone can see all blogs"""
    template_name = 'blog/templates/blog/blog_list_view.html'
    model = Blog
    context_object_name = 'blogs'


class BlogDetalView(DetailView):
    """Everyone can every blog with detail"""
    template_name = 'blog/templates/blog/blog_detail_view.html'
    model = Blog
    context_object_name = 'blog'


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Only authorized users can create new blog"""
    template_name = 'blog/templates/blog/blog_create_view.html'
    permission_required = ['accounts.can_create_blog', 'accounts.can_update_blog', 'accounts.can_delete_blog']
    # form_class = BlogModelForm
    model = Blog
    fields = ['author', 'title_image', 'title', 'content']
    context_object_name = 'blog'
    # slug_field = 'slug'
    # success_url = reverse_lazy('blog:blog_detail', kwargs={'slug': slug_field}, host='www')

    def get_success_url(self) -> str:
        print('current object:   ', self.object, '     slug field: ',self.object.slug)
        if self.object:
            url = rev('blog:blog_detail', kwargs={'slug': self.object.slug})
            # url = reverse('blog_detail', args=(self.object.slug), host='www')
            # print(reverse_host('www', args=('www',)))
            # url = reverse('blog:blog_list', host_args=('blog'), host='blog')
            # print(reverse_host('www', args=('',)))
            # url = reverse('blog:blog_list', host='www')
            print(url)
            # return reverse('blog:blog_detail', kwargs={'slug': self.slug_field}, host='www')
            return url
        return reverse('blog:blog_list', host='www')


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Only authorized users can Update a blog"""
    template_name = 'blog/templates/blog/blog_update_view.html'
    permission_required = ['accounts.can_create_blog', 'accounts.can_update_blog', 'accounts.can_delete_blog']
    form_class = BlogModelForm
    context_object_name = 'blog'
    slug_field = 'slug'
    success_url = reverse_lazy('blog:blog_detail', slug=slug_field, host='www')


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Only authorized users can delete a blog"""
    success_url = reverse_lazy('blog:blog_list', host='www')
    permission_required = ['accounts.can_create_blog', 'accounts.can_update_blog', 'accounts.can_delete_blog']


# Below views are test for html to pdf converter

# importing the necessary libraries
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf 

#Creating a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
         
        # getting the template
        pdf = html_to_pdf('blog/templates/blog/blog_pdf_test.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


# Another view to convert same html to pdf

from django.template.loader import get_template
from xhtml2pdf import pisa
from .process import link_callback

def render_pdf_view(request):
    template_path = 'blog/templates/blog/blog_pdf_test.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
