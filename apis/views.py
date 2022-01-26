from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filter

from core.models import Customer, Order
from .serializers import CustomerAdminSerializer, OrderAdminSerializer, UserSerializer, OrderUserSerializer
from .filters import OrderFilterset, CustomerFilterset , UserFilterset


class UserViewSet(ModelViewSet):
    """Viewset for User"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]
    # permission_classes = [AllowAny, ]
    filter_backends = [filter.DjangoFilterBackend, ]
    filter_class = UserFilterset

    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(self.queryset, many=True, context={'request': self.request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CustomerViewSet(ModelViewSet):
    """Viewset for Customer"""
    queryset = Customer.objects.all()
    serializer_class = CustomerAdminSerializer
    permission_classes = [IsAdminUser, ]
    # permission_classes = [AllowAny, ]
    filter_backends = [filter.DjangoFilterBackend, ]
    filter_class = CustomerFilterset
    # NOTE By default lookup_field based on 'pk'. For 'HyperlinkedModelSerializer' we should also set 'lookup_field'
    # argument in 'url' field in the Serializer. NOTE #
    lookup_field = 'name'


class OrderViewSet(ModelViewSet):
    """Viewset for Order"""
    queryset = Order.objects.all()
    serializer_class = OrderAdminSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [filter.DjangoFilterBackend, ]
    filter_class = OrderFilterset
    lookup_field = 'order_id'

    def list(self, request, *args, **kwargs):
        """Overwrite 'list' method of Viewset"""
        if not request.user.is_authenticated:
            OrderSerializer = OrderUserSerializer
        else:
            OrderSerializer = self.serializer_class
        name = request.GET.get('name', None)
        order_id = request.GET.get('order_id', None)
        # If order requested based on 'cutomer name': #
        if name and not order_id:
            order_customer_queryset = Order.objects.filter(customer__name__iexact=name)
            if order_customer_queryset.exists():
                order_cutomer_serializer = OrderSerializer(order_customer_queryset.all(), many=True, context={'request': request})
            else:
                # NOTE It is counter inituive but if we dont't set 'many' and 'context' argument for 'QUERYSET OBJECT'
                # even for a empty query, we will receive AssertionError for 'context' and AttributeError for 'many'. NOTE #
                # order_cutomer_serializer = OrderSerializer(order_customer_queryset.none(), many=True, context={'request': request})
                # Above command line returns empty list to client. But if we want to return some error directly to client we better use
                # below line:
                return Response(data={'error': 'Customer not found'}, status=status.HTTP_200_OK)
            return Response(data=order_cutomer_serializer.data, status=status.HTTP_200_OK)
        # If order requested based on 'order_id': #
        if order_id and not name:
            order_id_queryset = Order.objects.filter(order_id__iexact=order_id)
            print(order_id_queryset)
            if order_id_queryset.exists():
                # NOTE IMPORTANT: Only if we use 'QUERYSET OBJECTS' we should set 'many=True' arguement. For a
                # single model instance we 'MUST NOT' set 'many=True'. REMEMBER THIS. NOTE #
                order_id_serializer = OrderSerializer(order_id_queryset.first(), context={'request': request})
            else:
                # order_id_serializer = OrderSerializer(order_id_queryset.none(), many=True, context={'request': request})
                return Response(data={'error': 'Order not found'}, status=status.HTTP_200_OK)
            # To send better response to client, we better return our sole serializer without any additional information:
            # return Response(data={'order': order_id_serializer.data}, status=status.HTTP_200_OK) <==> below is better:
            return Response(data=order_id_serializer.data, status=status.HTTP_200_OK)
        # If order requested based on both 'customer name' and 'order_id': #
        if name and order_id:
            order_queryset = Order.objects.filter(cutomer_name=name, order_id=order_id)
            if order_queryset:
                order_queryset_serializer = OrderSerializer(order_queryset.first(), many=True, context={'request': request})
            else:
                order_queryset_serializer = OrderSerializer(order_queryset.none(), many=True, context={'request': request})
            return Response(data=order_queryset_serializer.data, status=status.HTTP_200_OK)
        # Or if user is admin show all orders to admin: #
        if self.request.user.is_authenticated:
            orders = Order.objects.all()
            order_serializer = OrderSerializer(orders, many=True, context={'request': request})
            return Response(data={'orders': order_serializer.data}, status=status.HTTP_200_OK)
        # If user in not authenticated as admin, Do not return any information from database to user: #
        else:
            return Response(data={'info': 'No order id or customer name entered'}, status=status.HTTP_200_OK)
