"""
To show or use some fields to admin without showing them to users, we can have two Serializers and
implement needed logic in each Serializers or in the 'view'. It might needs more time and be a tedious
job but it would be more secure and is more managable and straithforward.
https://www.django-rest-framework.org/api-guide/serializers/#serializer-inheritance

To show only some fields to client, we can use dynamic fields. This method requires little work but can be
very useful. Read below document for more information:
https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user_model

from core.models import Customer, Order


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for User model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail', lookup_field=get_user_model().USERNAME_FIELD)

    class Meta:
        model = get_user_model()
        fields = ['url', 'id', 'username', 'password', 'phone', 'email', 'is_superuser', 'is_admin', 'picture', 'background', 'first_name',
                  'last_name', 'name', 'date_joined']


class CustomerAdminSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Cutomer model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:customer-detail', lookup_field='name')
    # For HyperlinkedRelatedField that it's 'viewset' has 'lookup_field' on it, we must set it on the
    # field just like below field
    order_set = serializers.HyperlinkedRelatedField(read_only=True,
                                                    many=True,
                                                    view_name='api:order-detail',
                                                    lookup_field='order_id')

    class Meta:
        model = Customer
        # NOTE if we want to use 'serializer inheritance' later and also inherit Meta class of parent and we want
        # to use '__all__ fields, we better exclude EMPTY LIST instead of '__all__' for fields. NOTE #
        # fields = '__all__'
        exclude = []


class CustomerUserSerializer(CustomerAdminSerializer):
    """This Serializer used for ordinary users. It inherit all fields of parent except for 'url' field"""
    url = None

    class Meta(CustomerAdminSerializer.Meta):
        exclude = ['url', ]


class OrderAdminSerializer(serializers.HyperlinkedModelSerializer):
    """"Serializer for Order model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:order-detail', lookup_field='order_id')
    customer = CustomerAdminSerializer(read_only=True,
                                       many=False)
    customer_obj = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(),
                                                      many=False,
                                                      write_only=True,
                                                      allow_null=True,
                                                      help_text='This field used for DRF GUI'
                                                      )
    customer_name = serializers.CharField(write_only=True,
                                          allow_null=True,
                                          help_text='This field used for server-architecture model')
    # Because 'customer' have one to many relation with 'order', we cannot set 'many' attribute to 'True' in below fields or
    # we get this TypeError: "'customer' is not iterable" #
    # customer = CustomerAdminSerializer(many=False, read_only=True)
    """
    # Below field better used for the times we want to create a user ontime with creating order
    customer_data = CustomerAdminSerializer(write_only=True,
                                            many=False,
                                            allow_null=True,
                                            help_text='These fields used for server-architecture model')
    """
    class Meta:
        model = Order
        # fields = '__all__'
        exclude = []
    
    def __init__(self, instance=None, *args, **kwargs):
        """We can override this method to support for dynamically modifying fields."""
        print(kwargs)
        super().__init__(instance, *args, **kwargs)

    def create(self, validated_data):
        """'validated_data' is a dictionary consists of the data sent from client to serializer"""
        # First we must get 'additational fields' like 'customer_obj' and 'customer_data' data then
        # delete them. 'pop' method is the best way to do this in just one line: #
        customer_obj = validated_data.pop('customer_obj')
        # customer_data = validated_data.pop('customer_data')
        customer_name = validated_data.pop('customer_name')

        # First check if 'start' is not earlier than 'end' date:
        start = validated_data.get('start', None)
        end = validated_data.get('end', None)
        if start and end:
            if start > end:
                raise ValidationError(detail={'error': '"end" date could not be earlier than "start" date'}, code=status.HTTP_406_NOT_ACCEPTABLE)

        # If we want to create new order pythonic way or from 'DRF interface': #
        if customer_obj:
            validated_data.update({'customer': customer_obj})
            order = Order.objects.create(**validated_data)
            return order

        # If we want to create new user in server-client architectrue
        if customer_name:
            queryset = Customer.objects.filter(name=customer_name)
            if queryset.exists():
                customer = queryset.last()
                validated_data.update({'customer': customer})
                order = Order.objects.create(**validated_data)
                return order
            else:
                raise ValidationError(detail='Error: There is no customer with this name')
        
        # IF no customer_obj or customer_name entered raise error:
        else:
            raise ValidationError(detail={'Error': 'There is no customer identified'}, code=status.HTTP_400_BAD_REQUEST)

        """
        We used 'cutomer_name' to see if there is a customer with the entered name. So we don't need 'customer_data'
        field anymore...
        # To create a new order with any other 'API' technology like react or mobile apps: #
        # Delete all keys in 'customer_data' that their value are 'None'
        for k, v in dict(customer_data).items():
            if not v:
                customer_data.pop(k)
        if customer_data:
            customer = Customer.objects.filter(**customer_data).first()
            # NOTE: If we want, we can create new 'Customer' here with received data. NOTE #
            if not customer:
                raise ValidationError(detail={'error': 'There is no customer with this characteristics'}, code=status.HTTP_406_NOT_ACCEPTABLE)
            order = Order.objects.create(**validated_data, customer=customer)
            return order
        else:
            raise ValidationError(detail={'error': 'There is no user identified'}, code=status.HTTP_406_NOT_ACCEPTABLE)
        """

    def update(self, instance, validated_data):
        """Update any order"""
        customer_obj = validated_data.pop('customer_obj')
        # customer_data = validated_data.pop('customer_data')
        customer_name = validated_data.pop('customer_name')

        # Check if 'start' date is not later than 'end' date:
        start = validated_data.get('start', None)
        end = validated_data.get('end', None)
        if start and end:
            if start > end:
                raise ValidationError(detail={'error': '"end" date could not be earlier than "start" date'}, code=status.HTTP_406_NOT_ACCEPTABLE)

        # If we want to update order from DRF interface or pythonic way: #
        if customer_obj:
            instance.customer = customer_obj
            Order.objects.filter(id=instance.id).update(**validated_data)
            # After 'update' method on queryset, following method needed to get refreshed data from db per document:
            # NOTE https://docs.djangoproject.com/en/4.0/ref/models/instances/#refreshing-objects-from-database NOTE #
            instance.refresh_from_db()
            return instance

        # If we want to update order with server-client architecture
        if customer_name:
            queryset = Customer.objects.filter(name=customer_name)
            if queryset.exists():
                customer = queryset.last()
                validated_data.update({'customer': customer})
                Order.objects.filter(id=instance.id).update(**validated_data)
                instance.refresh_from_db()
                return instance
            else:
                raise ValidationError(detail='Error: There is no customer with this name')

        # If not 'customer_obj' selected or 'customer_name' entered raise Validation Error
        else:
            raise ValidationError(detail={'Error': 'There is no customer identified'}, code=status.HTTP_400_BAD_REQUEST)

        """
        # To update current order with any other 'API' technology like react or mobile apps: #
        if customer_data:
            # Delete all keys in 'customer_data' that their value are 'None'
            for k, v in dict(customer_data).items():
                if not v:
                    customer_data.pop(k)
            received_customer = Customer.objects.filter(name=customer_data['name'])
            # If customer data already is in database:
            if received_customer.exists():
                received_customer = received_customer.first()
                Customer.objects.filter(id=received_customer.id).update(**customer_data)
                received_customer.refresh_from_db()
                # If 'customer' field of the current order instance is not current 'customer':
                if instance.customer.id != received_customer.id:
                    instance.customer = received_customer
                    instance.save()
            else:
                new_customer = Customer.objects.create(**customer_data)
                instance.customer = new_customer
                instance.save()
            Order.objects.filter(id=instance.id).update(**validated_data)
            instance.refresh_from_db()
            instance.save()
            return instance
        # If no data about customer received, only update other fields except for 'customer' in order #
        else:
            Order.objects.filter(instance.id).update(**validated_data)
            instance.refresh_from_db()
            instance.save()
        """

class OrderUserSerializer(OrderAdminSerializer):
    """This Serializer used for ordinary users. It inherit all fields of parent except for 'url' field"""
    url = None
    # customer = None
    customer = CustomerUserSerializer(many=False, read_only=True)
    class Meta(OrderAdminSerializer.Meta):
        exclude = ['url', ]


class CustomerRequestSerializer(serializers.Serializer):
    """This Serializer used to get initial customer requests (serializer.Serializer used only for learning purpose)"""
    name = serializers.CharField()
    message = serializers.CharField()

    def create(self, validated_data):
        """serializer.Serializer does not have 'create' method by default. We should make the 'create' for it"""
        name = validated_data.get('name', None)
        message = validated_data.get('message', None)

        # If no 'name' or 'message' entered raise error:
        if not name:
            raise ValidationError(detail={'error': 'No name entered'})
        if not message:
            raise ValidationError(detail={'error': 'No message entered'})

        customer_qs = Customer.objects.filter(name=name)

        # If customer already exists just update the 'message' field:
        if customer_qs.exists():
            customer = customer_qs.first()
            customer.message = message
            customer.save()
        # If there is no customer with the name create a new user:
        else:
            customer = Customer.objects.create(**validated_data)
        
        return customer
