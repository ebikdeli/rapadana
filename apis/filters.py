from django_filters import rest_framework as filters

from core.models import Customer, Order


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
