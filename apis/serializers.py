from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user_model

from core.models import Customer, Order


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for User model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail')

    class Meta:
        model = get_user_model()
        fields = ['url', 'id', 'username', 'password', 'phone', 'email', 'is_superuser', 'is_admin', 'picture', 'background', 'first_name',
                  'last_name', 'name', 'date_joined']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Cutomer model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:customer-detail', lookup_field='name')

    class Meta:
        model = Customer
        fields = '__all__'
        lookup_field = 'name'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """"Serializer for Order model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:order-detail', lookup_field='order_id')
    # Because 'customer' have one to many relation with 'order', we cannot set 'many' attribute to 'True' in below fields or
    # we get this TypeError: "'customer' is not iterable" #
    customer = CustomerSerializer(many=False, read_only=True)
    customer_obj = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), many=False, write_only=True, allow_null=True)
    customer_data = CustomerSerializer(write_only=True)

    class Meta:
        model = Order
        fields = '__all__'
    
    def create(self, validated_data):
        """'validated_data' is a dictionary consists of the data sent from client to serializer"""
        # First we must get 'additational fields' like 'customer_obj' and 'customer_data' data then
        # delete them. 'pop' method is the best way to do this in just one line: #
        customer_obj = validated_data.pop('customer_obj')
        customer_data = validated_data.pop('customer_data')
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

    def update(self, instance, validated_data):
        """Update any order"""
        customer_obj = validated_data.pop('customer_obj')
        customer_data = validated_data.pop('customer_data')
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
            instance.save()
            return instance
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
