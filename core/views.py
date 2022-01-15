from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from order.models import Order
from .pgi import zarin_pay, zarin_verify


@login_required
def pay(request):
    """First step of payment. This view redirect user to pgi to enter his/her ID cart"""
    url = zarin_pay(request)
    return redirect(url)


def cart_pay(request):
    """It's the second step towards payment. After payment we should verify if payment was a success or not"""
    url = zarin_verify(request)
    return redirect(url)


@login_required
def receipt(request):
    """The last step toward payment. If every thing goes right user could see his/her order"""
    cart = request.user.cart.first()
    # Create new Order for the user and clean the cart
    Cart.objects.pay(request, cart)
    current_order = Order.objects.filter(cart=cart).first()
    # Or this:: current_order = Order.objects.filter(cart=request.user.cart.first()).first()
    # Or even simpler:: current_order = request.user.cart.first().orders.first()
    return render(request, 'order/templates/order/order_receipt.html', {'order': current_order})
