from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

from apps.core.models import Customer, Order


class UserFilterset(filters.FilterSet):
    """Filterset for User model"""
    
    class Meta:
        model = get_user_model()
        exclude = ['picture', 'background']


class CustomerFilterset(filters.FilterSet):
    """Filterset for Customer"""

    class Meta:
        model = Customer
        fields = '__all__'


class OrderFilterset(filters.FilterSet):
    """Filterset for Order"""

    class Meta:
        model = Order
        fields = '__all__'
