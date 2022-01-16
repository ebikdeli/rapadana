from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filter

from core.models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .filters import OrderFilterset, CustomerFilterset


class CustomerViewSet(ModelViewSet):
    """Viewset for Customer"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAdminUser, ]
    permission_classes = [AllowAny, ]
    filter_backends = [filter.DjangoFilterBackend, ]
    filter_class = CustomerFilterset


class OrderViewSet(ModelViewSet):
    """Viewset for Order"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [filter.DjangoFilterBackend, ]
    filter_class = OrderFilterset

    def list(self, request, *args, **kwargs):
        """Overwrite 'list' method of Viewset"""
        name = request.GET.get('name', None)
        order_id = request.GET.get('order_id', None)
        # If order requested based on 'cutomer name'
        if name and not order_id:
            order_customer_queryset = Order.objects.filter(customer_name=name)
            if order_customer_queryset.exists():
                order_cutomer_serializer = OrderSerializer(order_customer_queryset.all(), many=True, context={'request': request})
            else:
                order_cutomer_serializer = OrderSerializer(order_customer_queryset.none())
            return Response(data={'orders': order_cutomer_serializer.data}, status=status.HTTP_200_OK)
        # If order requested based on 'order_id'
        if order_id and not name:
            order_id_queryset = Order.objects.filter(order_id=order_id)
            if order_id_queryset:
                order_id_serializer = OrderSerializer(order_id_queryset.first(), context={'request': request})
            else:
                order_id_serializer = OrderSerializer(order_id_queryset.none())
            return Response(data={'order': order_id_serializer.data}, status=status.HTTP_200_OK)
        # If order requested based on both 'customer name' and 'order_id'
        if name and order_id:
            order_queryset = Order.objects.filter(cutomer_name=name, order_id=order_id)
            if order_queryset:
                order_queryset_serializer = OrderSerializer(order_queryset.first(), context={'request': request})
            else:
                order_queryset_serializer = OrderSerializer(order_queryset.none())
            return Response(data={'order': order_queryset_serializer.data}, status=status.HTTP_200_OK)
        # Or if user is admin show all orders to admin
        if self.request.user.is_authenticated:
            orders = Order.objects.all()
            order_serializer = OrderSerializer(orders, many=True, context={'request': request})
            return Response(data={'orders': order_serializer.data}, status=status.HTTP_200_OK)
        # If user in not authenticated as admin, Do not return any information from database to user.
        else:
            return Response(data={'info': 'No order id or customer name entered'}, status=status.HTTP_204_NO_CONTENT)
