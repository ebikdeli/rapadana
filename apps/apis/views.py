"""
Based on DRF documents, to get request data from 'GET' method we should use 'request.queryparams' instead of
'reqeust.GET' and in other methods like 'POST', 'PUT', 'PATCH' and etc we should use 'request.data' instead of
'request.POST':
https://www.django-rest-framework.org/api-guide/requests/#request-parsing 

This is how we query many to one relation (Or even one to one) relations
https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/#many-to-one-relationships

In DRF if want to get POST data, we better use 'request.data' rather than 'request.POST'.
https://www.django-rest-framework.org/api-guide/requests/#data

In Serializers only we use 'many=True' argument when our 'instance' argument is a QuerySet even if the queryset
is 'empty'. But if we want to use a model instance we should set 'many=False'.
"""
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters import rest_framework as filter

from apps.core.models import Customer, Order
from .serializers import CustomerAdminSerializer, OrderAdminSerializer, UserSerializer,\
                         OrderUserSerializer, CustomerRequestSerializer
from .filters import OrderFilterset, CustomerFilterset , UserFilterset


class UserViewSet(ModelViewSet):
    """Viewset for User"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]
    # permission_classes = [AllowAny, ]
    filter_backends = [filter.DjangoFilterBackend, ]
    filter_class = UserFilterset
    lookup_field = get_user_model().USERNAME_FIELD

    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(self.queryset, many=True, context={'request': request})
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

    def get_queryset(self):
        """Override this method to make the program faster"""
        return Order.objects.all()

    def get_serializer_class(self):
        """Override get_serilalizer_class to get the right serializer based on 'user' authorization status"""
        if not self.request.user.is_authenticated:
            return OrderUserSerializer
        else:
           return OrderAdminSerializer

    def list(self, request, *args, **kwargs):
        """Overwrite 'list' method of Viewset"""
        Serializer = self.get_serializer_class()
        # name = request.GET.get('name', None)
        # order_id = request.GET.get('order_id', None)
        # This is better and more standard way to receive GET parameter
        name = self.request.query_params.get('name', None)
        order_id = request.query_params.get('order_id', None)

        # If order requested based on 'cutomer name': #
        if name and not order_id:
            order_customer_queryset = self.get_queryset().filter(customer__name__iexact=name)[:1]
            if order_customer_queryset.exists():
                order_cutomer_serializer = Serializer(order_customer_queryset, many=True, context={'request': request})
            else:
                # NOTE It is counter inituive but if we dont't set 'many' and 'context' argument for 'QUERYSET OBJECT'
                # even for a empty query, we will receive AssertionError for 'context' and AttributeError for 'many'. NOTE #
                order_cutomer_serializer = Serializer(order_customer_queryset.none(), many=True, context={'request': request})
                return Response(data=order_cutomer_serializer.data, status=status.HTTP_204_NO_CONTENT)
                # Above command line returns empty list to client. But if we want to return some error directly to client we better use
                # below line:
                # return Response(data={'error': 'Customer not found'}, status=status.HTTP_200_OK)
            return Response(data=order_cutomer_serializer.data, status=status.HTTP_200_OK)

        # If order requested based on 'order_id': #
        if order_id and not name:
            order_id_queryset = self.get_queryset().filter(order_id__iexact=order_id)
            if order_id_queryset.exists():
                # NOTE IMPORTANT: Only if we use 'QUERYSET OBJECTS' we should set 'many=True' arguement. For a
                # single model instance we 'MUST NOT' set 'many=True'. REMEMBER THIS. NOTE #
                order_id_serializer = Serializer(order_id_queryset.first(), context={'request': request})
            else:
                order_id_serializer = Serializer(order_id_queryset.none(), many=True, context={'request': request})
                return Response(data=order_id_serializer.data, status=status.HTTP_204_NO_CONTENT)
                # return Response(data={'error': 'Order not found'}, status=status.HTTP_200_OK)
            # To send better response to client, we better return our sole serializer without any additional information:
            # return Response(data={'order': order_id_serializer.data}, status=status.HTTP_200_OK) <==> below is better:
            return Response(data=order_id_serializer.data, status=status.HTTP_200_OK)

        # If order requested based on both 'customer name' and 'order_id': #
        if name and order_id:
            order_queryset = self.get_queryset().filter(customer__name=name, order_id=order_id)
            if order_queryset.exists():
                order_queryset_serializer = Serializer(order_queryset.first(), many=False, context={'request': request})
            else:
                order_queryset_serializer = Serializer(order_queryset.none(), many=True, context={'request': request})
            print(order_queryset_serializer)
            return Response(data=order_queryset_serializer.data, status=status.HTTP_204_NO_CONTENT)

        # Or if user is authenticated show all orders to authenticated user (In the program logic, all user are admin!):
        if self.request.user.is_authenticated:
            orders = self.get_queryset()
            order_serializer = Serializer(orders, many=True, context={'request': request})
            return Response(data={'orders': order_serializer.data}, status=status.HTTP_200_OK)

        # If user in not authenticated as admin, Do not return any information from database to user: #
        else:
            return Response(data={'info': 'No order id or customer name entered'}, status=status.HTTP_200_OK)


class CustomerRequest(APIView):
    """Simple API view to get customer request and save data in database (APIView just used for learning purpose)"""
    def get(self, request, format=None):
        return Response(data='This api working perfectly', status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # name = request.POST.get('name', None)
        # message = request.POST.get('message', None)

        name = request.data.get('name', None)
        message = request.data.get('message', None)

        if not name:
            return Response(data={'Error': 'No name received'}, status=status.HTTP_400_BAD_REQUEST)
        if not message:
            return Response(data={'Error': 'No message enterd'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CustomerRequestSerializer(instance=None, data={'name': name, 'message': message})
        serializer.is_valid()
        # print(serializer.validated_data)
        serializer.save()
        # print(serializer.data)
        return Response(data={'success': 'Data successfully received'}, status=status.HTTP_200_OK)
