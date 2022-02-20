"""
When using SessionBased authentication, any request method other than 'get' we need 'csrf token' to
authenticate user session. To do that we need to get 'csrftoken' cookie we can
"""
from django.shortcuts import redirect
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
    return JsonResponse(data=data, safe=False)
    # return redirect(data)
