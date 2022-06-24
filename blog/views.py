from django.shortcuts import render, HttpResponse


def some_blog(request):
    return HttpResponse("<h1>Subdomain blog just works!</h1>")
