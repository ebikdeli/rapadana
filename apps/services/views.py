from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count, Sum

from .models import Service


def service_index(request):
    return HttpResponse(content='<div align="center"><h1>Service app working just fine! این سرویس به خوبی کار می کند!</h1></div>')


def service_select(request):
    """if request.method == 'POST':
        data = request.POST
        print(data)
        data = dict(data)
        data.pop('csrfmiddlewaretoken')
        print(data)
        if not data:
            return HttpResponse('<div align="center"><h1>دیتای خوب وارد کنید!</h1></div>')
        for d, v in data.items():
            print(d, ' -->  ', v)
            # Process received service_id codes
            servieces_id_list = data['services']
            services = Service.objects.filter(id__in=servieces_id_list)
            return redirect('services:service_order')"""
    
    services = Service.objects.all()
    r = render(request, 'services/templates/services/service_select.html', {'services': services})
    # print(r, '    ', type(r))
    return r


def service_order(request):
    # return HttpResponse('<div align="center"><h1>موفق شدید!</h1></div>')
    if request.method == 'POST':
        data = request.POST
        # print(data)
        data = dict(data)
        data.pop('csrfmiddlewaretoken')
        # print(data)
        if not data:
            return HttpResponse('<div align="center"><h1>دیتای خوب وارد کنید!</h1></div>')
        for d, v in data.items():
            # print(d, ' -->  ', v)
            # Process received service_id codes
            servieces_id_list = data['service_id']
            services = Service.objects.filter(id__in=servieces_id_list)

            # Some simple toturial for django Aggregation and Annotation

            # print('aggregate:   ', services.aggregate(Count('price')))

            # annot = services.all()
            # print('annotate:   ', annot, '  type: ', type(annot), '   ', annot[0], '  type: ', type(annot[0]), '  ', annot[0].price__count)

            # 2 Above line cause this error:
            # AttributeError: 'Service' object has no attribute 'price__count'
            # To solve the problem we can use 2 below lines:

            # annot = services.annotate(Count('price'))
            # print('annotate:   ', annot, '  type: ', type(annot), '   ', annot[0], '  type: ', type(annot[0]), '  ', annot[0].price__count)

            tp = services.aggregate(total_price=Sum('price'))
            # If we use this line instead of above: tp = services.aggregate(total_price=Sum('price'))
            # we can't use 'total_price' variable like below. Instead of 'total_price' we should had used 'price__sum'
            # The default pattern is (if we don't assign an arbitray variable like 'total_price'):
            # "<field_name>__<aggregate_model(in lower case)>"
            # print(tp)
            # print('total_price:', tp['total_price'])
            total_price = int(tp['total_price'])

            context = {'services': services, 'total_service': len(servieces_id_list), 'total_price': total_price}
            return render(request=request, template_name='services/templates/services/service_order.html', context=context)


def service_order_verify(request):
    print(request.POST)
    print(dict(request.POST))
    return JsonResponse(data=dict(request.POST))
