"""
    This code writen for ZarinPal pgi, but we can use it for any REST pgi service with minimal changes.
    Note: Using 'global variables' increases the risk of process race between users and expose a user data
    to other users. In 2 ways we can solve this issue: 1- Using 'session' to save the data needed between
    multiple views in session based authentication and 2- Use additional headers or variables in token based
    authentication.
"""
from django.conf import settings

from .models import Customer, Order

import requests
import json

# This is 'heroku' callback url
CALLBACK_URL = 'https://rapdana.herokuapp.com/api/pay/cart/'
# This is local callback url
# CALLBACK_URL = 'http://127.0.0.1:8000/api/pay/cart/'
if not settings.DEBUG:
    # This is website callback url
    CALLBACK_URL = 'https://www.example/api/pay/cart/'
ZARIN_MERCHANT_ID = 'b46922ec-f436-402b-a553-4107451475cc'

NAME = ''
ORDER_ID = ''
PRICE = 0

def zarin_response_code(request, zarin_response):
    """Helper function to decode if any error messages in payment process"""
    code = zarin_response['errors']['code']
    if code == -9:
        error = 'موجودی باید بیش از 1000 ریال بشد'
    elif code == -10:
        error = 'آدرس آی پی یا مرچنت کد پذیرنده صحیح نیست'
    elif code == -12:
        error = 'تلاش بیش از اندازه در یک بازه زمانی کوتاه. بعدا تلاش کنید'
    elif code == -34:
        error =  'مبلغ وارد شده از تراکنش بیشتر است'
    elif code == -51:
        error = 'پرداخت ناموفق'
    elif code == -53:
        error = 'کد اتوریتی نامعتبر است'
    return error


def zarin_pay_verify(request, authority, pay):
    """Helper function used to verify the payment"""
    url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
    data = {
        'merchant_id': ZARIN_MERCHANT_ID,
        # 'amount': int(pay) * 10,
        'amount': 1000,
        'authority': authority
            }
    headers = {'accept': 'application/json',
               'content-type': 'application/json'}
    r = requests.post(url=url, data=json.dumps(data), headers=headers)
    if r.status_code == 200 or 201:
        zarin_response = r.json()
        if zarin_response['data']:
            return {'verify': f'تاییدیه تراکنش شما: {authority}'}
        else:
            error = zarin_response_code(request, zarin_response)
            return {'error': error}


def zarin_pay(request):
    """Initialize payment process and redirect user to pgi"""
    # It should get two data from client: 1-'customer name' 2-'order_id'
    # user = request.user
    # cart = user.cart.first()
    if request.method == 'GET':
        customer_name = request.GET.get('name', None)
        order_id = request.GET.get('order_id', None)
        if not customer_name:
            # return JsonResponse(data={'request error': 'No customer name received'}, safe=False)
            data={'error': 'No customer name received'}
            return data
        if not order_id:
            # return JsonResponse(data={'request error': 'No order_id received'}, safe=False)
            data={'error': 'No order_id received'}
            return data
        # customer = Customer.objects.filter(name__icontain=customer_name)
        customer = Customer.objects.filter(name__iexact=customer_name)
        if not customer.exists():
            # return JsonResponse(data={'error': 'There is no customer with the requested name'}, safe=False)
            data={'error': 'There is no customer with the requested name'}
            return data
        order = Order.objects.filter(order_id=order_id)
        if not order.exists():
            # return JsonResponse(data={'error': 'There is no order registered with requested id'}, safe=False)
            data={'error': 'There is no order registered with requested id'}
            return data
        customer = customer.first()
        order = order.first()
        # global NAME; NAME = customer_name
        # global ORDER_ID; ORDER_ID =order_id
        request.session['name'] = customer_name
        request.session['order_id'] = order_id
        if not customer.email:
            customer.email = 'ثبت نشده'
        # if not user.email:
            # user.email = 'ثبت نشده'
        if not customer.phone:
            customer.phone = 'ثبت نشده'
        # if not user.phone:
            # user.phone = 'ثبت نشده'
        url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
        headers = {'accept': 'application/json',
                'content-type': 'application/json'}
        data = {
            'merchant_id': ZARIN_MERCHANT_ID,
            # 'amount': int(order.pay) * 10,
            'amount': 1000,
            'description': f'هزینه طراحی برنامه تحت وب',
            'callback_url': CALLBACK_URL,
            'metadata': {'email': customer.email,
                         'phone': customer.phone}
                }
        try:
            r = requests.post(url=url, data=json.dumps(data), headers=headers)
        except requests.ConnectionError:
            # return JsonResponse(data={'برقراری با ارتباط با واسط پرداخت به مشکل برخورده'}, safe=True)
            data={'برقراری با ارتباط با واسط پرداخت به مشکل برخورده'}
            return data
        if r.status_code == 200 or 201:
            zarin_response = r.json()
            # If request was a success:
            if zarin_response['data']:
                authority = zarin_response['data']['authority']
                new_url = f'https://www.zarinpal.com/pg/StartPay/{authority}'
                # Redirect user to PGI to pay
                # return JsonResponse(data={'url': new_url})
                data={'url': new_url}
                return data
            # If there is a error:
            else:
                error = zarin_response_code(request, zarin_response)
                # return JsonResponse(data={'error': error})
                data={'error': error}
                return data
        else:
            # return JsonResponse(data={'error': 'ارتباط با سایت پذیرنده ممکن نمی باشد'}, safe=False)
            data={'error': 'ارتباط با سایت پذیرنده ممکن نمی باشد'}
            return data
    else:
        # return JsonResponse(data={'error': 'only "GET" method could be used'}, safe=False)
        data={'error': 'only "GET" method could be used'}
        return data


def zarin_verify(request):
    """Used in the last step to verify the payment then redirect user to receipt"""
    data = request.GET
    authority = data['Authority']
    # global ORDER_ID
    # order = Order.objects.get(order_id=ORDER_ID)
    order = Order.objects.get(order_id=request.session['order_id'])
    # Helper method called
    response = zarin_pay_verify(request, authority, order.pay)
    from core.signals import generate_random_id
    order.authority = authority
    order.peigiry = generate_random_id(6)
    order.remain = order.remain - order.pay
    if order.remain == 0:
        order.is_paid = True
    order.save()
    if data['Status'] == 'OK':
        # return JsonResponse(data={'success': 'سفارش شما با موفقیت ثبت شد.'}, safe=False)
        data={'success': 'سفارش شما با موفقیت ثبت شد.'}
        data.update(response)
        print(data)
        return data
    if data['Status'] == 'NOK':
        # return JsonResponse(data={'error': 'پرداخت انجام نگرفت و سفارشی ثبت نگردید'}, safe=False)
        data={'success': 'پرداخت انجام گرفت اما تاییدیه صادر نشد'}
        data.update(response)
        print(data)
        return data


"""
    Note that we should not use 'redirect' function in helper modules. Else we get
    ValueError None type object error.
"""
