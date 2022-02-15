"""
For Charfields, Slugfields, Textfields and any other fields that saved as 'STRING' or 'CHAR' field in database,
to set the field optional we can only use 'blank=True' without set 'null=True'. This way the field saved into db
by a mere empty string or ''. But for other types to set the field optional we need to set both the arguments True.
"""
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """This model represents Customer. It is simple and basic"""
    name = models.CharField(verbose_name=_('customer name'), max_length=100, unique=True)
    email = models.EmailField(verbose_name=_('customer email'), blank=True)
    address = models.TextField(verbose_name=_('customer address'), blank=True)
    phone = models.CharField(verbose_name=_('customer phone number'),
                             max_length=13,
                             blank=True,
                             validators= [MaxLengthValidator(13, _('phone number is too long')),
                                          MinLengthValidator(11, _('phone number length is too short'))])
    slug = models.SlugField(verbose_name=_('slug'), blank=True)
    created = models.DateTimeField(verbose_name=_('customer joined'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('customer specs updated'), auto_now=True)

    def __str__(self):
        if self.name:
            return f'customer({self.id})- {self.name}'
        return f'customer({self.id})'


class Order(models.Model):
    """Model for customer orders. This model built by Admin"""
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE,
                                                  verbose_name=_('customer'),
                                                  blank=True,
                                                  null=True)
    content = models.TextField(verbose_name=_('contents'), blank=True, null=True)
    order_id = models.CharField(verbose_name=_('order id'), max_length=10, blank=True)
    authority = models.CharField(verbose_name=_('authority code'), max_length=50, blank=True)
    peigiry = models.CharField(verbose_name=_('peigiry code'), max_length=6, blank=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=12, decimal_places=0, default=-1)
    pay = models.DecimalField(verbose_name=_('current payment'), max_digits=12, decimal_places=0, default=-1)
    remain = models.DecimalField(verbose_name=_('remain price'), max_digits=12, decimal_places=0, default=-1)
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    start = models.DateField(verbose_name=('project start date'), blank=True, null=True)
    end = models.DateField(verbose_name=_('project end time(est)'), blank=True, null=True)
    is_ready = models.BooleanField(verbose_name=_('project ready'), default=False)
    is_delivered = models.BooleanField(verbose_name=_('project delivered to customer'), default=False)
    slug = models.SlugField(verbose_name=_('slug'), blank=True)
    created = models.DateTimeField(verbose_name=_('order created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('order updated'), auto_now=True)

    def __str__(self):
        if self.customer.name:
            return 'order(' + str(self.id) + '): ' + self.customer.name
        return 'order(' + str(self.id) + ')'
