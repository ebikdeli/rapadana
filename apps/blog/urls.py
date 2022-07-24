from django.urls import path
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import BlogSitemap


app_name = 'blog'

sitemaps = {'blogs': BlogSitemap}

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('update/<slug:slug>/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<slug:slug>/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('<slug:slug>/', views.BlogDetalView.as_view(), name='blog_detail'),
    path('comment/create/<str:blog_slug>', views.comment_blog_create, name='comment_blog_create'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),

    # This is a test for html to pdf converter
    path('pdf1/', views.GeneratePdf.as_view()),
    path('pdf2/', views.render_pdf_view),
]
