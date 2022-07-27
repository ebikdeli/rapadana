from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, DetailView, CreateView,\
    UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse as rev
from django_hosts.resolvers import reverse_lazy, reverse, reverse_host

from .models import Blog, Comment
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
            # url = rev('blog:blog_detail', kwargs={'slug': self.object.slug})
            print(reverse_host('www', args=('www',)))
            
            # url = reverse(viewname='blog:blog_detail', kwargs={'slug': self.object.slug}, host_args=('www',), host='www', scheme='http', port='8000')
            url = reverse(viewname='blog:blog_detail', kwargs={'slug': self.object.slug}, host_args=('www',), host='www',
                          scheme=settings.MAIN_SCHEME, port=str(settings.MAIN_PORT))
            # print(reverse_host('www', args=('www',)))
            # url = reverse('blog:blog_list', host_args=('blog'), host='blog')
            # print(reverse_host('www', args=('',)))
            # url = reverse('blog:blog_list', host='www')
            print(url)
            # return reverse('blog:blog_detail', kwargs={'slug': self.slug_field}, host='www')
            return url
        return reverse('blog:blog_list', host='www', host_args=('www',), scheme=settings.MAIN_SCHEME, port=str(settings.MAIN_PORT))


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Only authorized users can Update a blog"""
    template_name = 'blog/templates/blog/blog_update_view.html'
    permission_required = ['accounts.can_create_blog', 'accounts.can_update_blog', 'accounts.can_delete_blog']
    form_class = BlogModelForm
    queryset = Blog.objects.all()
    context_object_name = 'blog'
    slug_field = 'slug'

    def get_success_url(self) -> str:
        success_url = reverse('blog:blog_detail', kwargs={'slug': (self.object.slug)}, host='www', host_args=('www',), scheme=settings.MAIN_SCHEME, port=str(settings.MAIN_PORT))
        return success_url
    # success_url = reverse_lazy('blog:blog_detail', kwargs={'slug': (get_slug_field())}, host='www', host_args=('www',), scheme=settings.MAIN_SCHEME, port=str(settings.MAIN_PORT))


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Only authorized users can delete a blog"""
    success_url = reverse_lazy('blog:blog_list', host='www', host_args=('www',), scheme=settings.MAIN_SCHEME, port=str(settings.MAIN_PORT))
    permission_required = ['accounts.can_create_blog', 'accounts.can_update_blog', 'accounts.can_delete_blog']


class CommentBlogDetailView(DetailView):
    """View each comment detail (not so functional!)"""
    template_name: str = 'blog/templates/comment/comment_blog_detail.html'
    model = Comment
    context_object_name = 'comment'


def comment_blog_create(request, blog_slug=None):
    """Create new comment for blog"""
    if not blog_slug:
        return HttpResponse(content="<div align='center'><h1>وبلاگی انتخاب نشده</h1></div>")

    if request.method == "POST":
        if not request.POST:
            return HttpResponse('<div align="center"><h1>هیچ کامنتی وارد نشده</h1></div>')
        
        # Proccess received data
        data = dict(request.POST)
        csrf_token = data.pop('csrfmiddlewaretoken')[0]
        blog_id = data['blog_id'][0]
        name = data['name'][0]
        content = data['content'][0]
        user = request.user if request.user.is_authenticated else None

        # Get parent comment if there is any
        parent_comment_id = data['comment_id'][0] if data['parent_comment_id'][0] else None
        parent_comment = None
        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id) if Comment.objects.filter(id=parent_comment_id).exists() else None
            
        # Get the blog specs we want add the new comment to it
        blog = Blog.objects.get(id=blog_id)
        blog_ct = ContentType.objects.get_for_model(Blog)   # Or: ContentType.objects.get_for_model(app_label='blog', model='blog')

        # Create comment
        comment = Comment.objects.create(sub=parent_comment,
                                         user=user,
                                         name=name,
                                         session_id=request.session.session_key,
                                         ip_v4 = request.session['ip_v4'],
                                         content=content,
                                         content_type=blog_ct,
                                         object_id=blog.id)
        # comment = Blog.objects.get(id=blog_id).comments.create(sub=parent_comment_id, user=user, content=content)  <== This one is no good
        print(comment, '    ', comment.content)
        # Redirect user back to the last blog
        return redirect('blog:blog_detail', slug=blog_slug)
    
    else:
        return JsonResponse(data={'Status': 'NOK', 'error': f'"{request.method}" does not supported'}, safe=False)


def comment_blog_update(request, blog_slug=None):
    """Update the blog created by user"""
    if not blog_slug:
        return HttpResponse('<div align="center"><h1>هیچ کامنتی وارد نشده</h1></div>')

    if request.method == 'POST':
        # Proccess received data
        data = dict(request.POST)
        csrf_token = data.pop('csrfmiddlewaretoken')[0]
        # blog_id = data['blog_id'][0]
        name = data['name'][0]
        content = data['content'][0]
        user = request.user if request.user.is_authenticated else None
        comment_id = data['comment_id'][0]

        # Get parent comment if there is any
        parent_comment_id = data['comment_id'][0] if data['parent_comment_id'][0] else None
        parent_comment = None
        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id) if Comment.objects.filter(id=parent_comment_id).exists() else None

        # Enforce the received changes and update the comment
        comment = Comment.objects.get(id=comment_id)
        if not comment.user:
            comment.user = user
        if parent_comment:
            comment.sub = parent_comment
        comment.update(name=name, content=content)
        comment.refresh_from_db()
        print(comment)
        # Redirect user back to the last blog
        return redirect('blog:blog_detail', slug=blog_slug)

    else:
        return JsonResponse(data={'Status': 'NOK', 'error': f'"{request.method}" does not supported'}, safe=False)


def comment_blog_delete(request, blog_slug=None):
    """Delete the comment by the writer"""
    if not blog_slug:
        return HttpResponse('<div align="center"><h1>هیچ کامنتی وارد نشده</h1></div>')

    if request.method == 'POST':
        # Process received data
        data = dict(request.POST)
        comment_id = data['comment_id'][0]

        # Query the comment with received 'id' then delete it
        Comment.objects.get(id=comment_id).delete()
        print('comment deleted')
        # Redirect user back to the last blog
        return redirect('blog:blog_detail', slug=blog_slug)

    else:
        return JsonResponse(data={'Status': 'NOK', 'error': f'"{request.method}" does not supported'}, safe=False)




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
