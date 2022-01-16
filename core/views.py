from django.shortcuts import redirect
from django.http import JsonResponse
from .pgi import zarin_pay, zarin_verify


# @login_required
def pay(request):
    """First step of payment. This view redirect user to pgi to enter his/her ID cart"""
    data = zarin_pay(request)
    if 'url' in data.keys():
        return redirect(data['url'])
    return JsonResponse(data=data, safe=False)


def cart_pay(request):
    """It's the second step towards payment. After payment we should verify if payment was a success or not"""
    data = zarin_verify(request)
    return JsonResponse(data=data, safe=False)
    # return redirect(data)
