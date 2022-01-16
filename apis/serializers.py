from rest_framework import serializers

from core.models import Customer, Order


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Cutomer model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:customer-detail')

    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """"Serializer for Order model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:order-detail')
    # Because 'customer' have one to many relation with 'order', we cannot set 'many' attribute to 'True' in below fields or
    # we get this TypeError: "'customer' is not iterable"
    customer = CustomerSerializer(many=False, read_only=True)
    customer_data = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), many=False, write_only=True)

    class Meta:
        model = Order
        fields = '__all__'
