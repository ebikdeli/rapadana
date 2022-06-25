from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list_view'),
    path('pdf1/', views.GeneratePdf.as_view()),
    path('pdf2/', views.render_pdf_view),
]
