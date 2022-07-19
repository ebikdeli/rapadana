from django.shortcuts import render, HttpResponse


def service_index(request):
    return HttpResponse(content='<div align="center"><h1>Service app working just fine! این سرویس به خوبی کار می کند!</h1></div>')
