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

    class Meta:
        model = Order
        fields = '__all__'
