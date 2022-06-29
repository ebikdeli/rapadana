from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('update/<slug:slug>/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<slug:slug>/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('<slug:slug>/', views.BlogDetalView.as_view(), name='blog_detail'),

    # This is a test for html to pdf converter
    path('pdf1/', views.GeneratePdf.as_view()),
    path('pdf2/', views.render_pdf_view),
]
