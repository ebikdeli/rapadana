from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum
from django.views.generic import ListView, TemplateView, FormView
from django.core.exceptions import ValidationError

import decimal

from .models import OrderService, Service


def service_index(request):
    return HttpResponse(content='<div align="center"><h1>Service app working just fine! این سرویس به خوبی کار می کند!</h1></div>')


class ServiceSelectList(ListView):
    """Customer can see all services"""
    template_name = 'services/templates/services/service_select.html'
    model = Service
    context_object_name = 'services'


# THIS IS FOR TOTURIAL PURPOSES
# def service_select(request):
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
    
#    services = Service.objects.all()
#    r = render(request, 'services/templates/services/service_select.html', {'services': services})
    # print(r, '    ', type(r))
#    return r


# @method_decorator(login_required, name='dispatch')
class ServiceOrderList(ListView):
    """Show ordered services to verify or discard them"""
    template_name: str= 'services/templates/services/service_order.html'
    model = Service
    context_object_name = 'services'
    i = 0

    def get_context_data(self, **kwargs):
        """Override this method to process received data from 'GET' method"""
        context = super().get_context_data(**kwargs)
        # Parse 'GET' data from 'ServiceSelectList' view
        get_data = self.request.GET
        get_data = dict(get_data)
        if not get_data:
            context['has_data'] = False
            # If there is no data in response, terminate the process
            return context

        # Process received service_id codes
        services_id_list = get_data['service_id']
        services = Service.objects.filter(id__in=services_id_list)

        # Raise bad data flag if 'services' has bad request
        if not services.exists():
            context['has_data'] = False
            return context

        # Count 'total_service' and 'total_price' to send to the template
        tp = services.aggregate(total_price=Sum('price'))
        context.update({'has_data': True,
                       'services': services,
                       'total_price': int(tp['total_price']),
                       'total_service': len(services)})
        return context

    def dispatch(self, request, *args, **kwargs):
        """NOTE: 'dispatch' is one of the earliest methods in generic method that invoke. If we want to do something
        special with our method, like this 'ListView' that doesn't have 'post' method, we can use 'dipatch' to get
        what we want.
        If we want to invoke some method that not implemented in the Generic view by default, 'dispatch' is the place
        we can do that."""
        if request.method == 'POST':
            # If no data in 'POST' response, invoke below following condition
            if not request.POST:
                return HttpResponse("<div align='center'><h1>پس چرا هیچ دیتایی نیست؟؟؟؟؟؟؟</h1></div>")
            data_post = dict(request.POST)
            csrf_token = data_post.get('csrfmiddlewaretoken', None)

            # Process received data and put them in database for the user
            services = Service.objects.filter(id__in=data_post['service_id'])
            if not services.exists():
                return HttpResponse("<div align='center'><h1>دیتا هست اما بد هست</h1></div>")
            # Create order_service for the services received
            user = request.user if request.user.is_authenticated else None
            order_service = OrderService(
                customer = user,
                total_service = int(request.POST['total_service_number']),
                price = decimal.Decimal(data_post['total_price'][0].replace(',', ''))
            )
            order_service.save()
            for service in services:
                order_service.service.add(service)
            return redirect('services:order_verify', order_uuid=str(order_service.order_uuid))

        # For other method except for 'POST' follow regular precedure
        return super().dispatch(request, *args, **kwargs)


# THIS IS FOR TOTURIAL PURPOSES
"""
def service_order(request):
    if request.method == 'GET':
        data = request.GET
        print('GET: ', request.GET)
        # print(data)
        data = dict(data)
        # data.pop('csrfmiddlewaretoken')
        print(data)
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
"""


class ServiceOrderVerify(TemplateView):
    """Verify the services ordered from 'ServiceOrderList'."""
    template_name = 'services/templates/services/service_order_verify.html'

    def get_context_data(self, **kwargs):
        """Override this method to be able parse 'order_uuid' received from 'url' and get right 'OrderService' object"""
        context = super().get_context_data(**kwargs)
        try:
            order_uuid = kwargs.get('order_uuid', None)
            if order_uuid:
                order_service_qs = OrderService.objects.filter(order_uuid=order_uuid)
                print(order_service_qs)
                if order_service_qs.exists():
                    order_service = order_service_qs.first()
                    context['order_service'] = order_service
                    return context
            # If there is any problem return None for 'order_service'
            context['order_service'] = None
            return context

        # Because parsing 'uuid' field may raise 'validation error' in django, we do not let the program stopped
        except(ValidationError, ValueError):
            context['order_service'] = None
            return context


# THIS IS FOR TOTURIAL PURPOSES
"""
def service_order_verify(request):
    print(request.POST)
    print(dict(request.POST))
    return JsonResponse(data=dict(request.POST))
"""
