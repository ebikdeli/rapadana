"""
** In client-server architecture, to send arbitrary data to some client without the client asking for any
api then redirect users to a good url the client wants, we have to send the data to client through HTTP HEADERS
because there is no way to send arbitrary data to client without affecting user experience.

** We are using 'redirect' function in 'cart_pay' view to redirect user to the 'index' page of client.
It's important to remember 'redirect' returns 'HttpRedirectResponse' instance that is a subclass of
'HttpResponse' - JSONResponse is also subclass of HttpResponse - and we can add custom 'Headers' to
it their instance and return them to client. 'render' works this way too.
https://docs.djangoproject.com/en/4.0/ref/request-response/#django.http.HttpResponse.headers
NOTE: Remember that HTTP HEADERS do not accept non-ascii headers.

** When using SessionBased authentication, any request method other than 'get' we need 'csrf token' to
authenticate user session. To do that we need to get 'csrftoken' cookie value (We can get this cookie
in browser -> Network(tab) -> Request(tab) -> Headers -> Cookies -> csrftoken) and send it in the
request header as 'X-CSRFToken' header. To test it we can add a header in 'postman'.
Read documents below for more information:
https://www.django-rest-framework.org/topics/ajax-csrf-cors/#csrf-protection
https://docs.djangoproject.com/en/4.0/ref/csrf/#setting-the-token-on-the-ajax-request
"""
from django.shortcuts import redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .pgi import zarin_pay, zarin_verify


# @login_required
@csrf_exempt
def pay(request):
    """First step of payment. This view redirect user to pgi to enter his/her ID cart"""
    # This is the url we begin our payment proccedure. We need two arguments to begin payment:
    # https://rapdana.herokuapp.com/api/pay?name=ehsan&order_id=4W8SSVQXES
    data = zarin_pay(request)
    if 'url' in data.keys():
        return redirect(data['url'])
    return JsonResponse(data=data, safe=False)


@csrf_exempt
def cart_pay(request, order_id=None):
    """It's the second step towards payment. After payment we should verify if payment was a success or not"""
    data = zarin_verify(request, order_id)
    url_redirect_to = 'https://react-test-eosin.vercel.app/'
    response = redirect(url_redirect_to)

    # We can either send the data as a dictionary or send them seprately:
    # 1- Seprately
    # for k, v in data.items():
    #     response.headers[k] = v
    # 2- As dictionary
    response.headers['payment_response'] = data
    response.headers['status'] = data['status']
    # We now redirect customer to main page

    return response
    # return JsonResponse(data=data, safe=False)
