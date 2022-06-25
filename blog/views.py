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
