from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from djmoney.models.fields import MoneyField

import uuid


class Category(models.Model):
    """Model for category"""
    sub = models.ForeignKey('self',
                            verbose_name=_('sub category'),
                            on_delete=models.CASCADE,
                            related_name='category_sub',
                            blank=True,
                            null=True)
    name = models.CharField(verbose_name=_('name'), max_length=30)
    slug = models.SlugField(verbose_name=_('slug'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if self.sub:
            return f'{self.sub.name}_{self.name}'
        return f'{self.name}'

    def save(self, *args, **kwargs) -> None:
        """Overriding 'save' method to fill 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Model for every service for every website client requests"""
    name = models.CharField(verbose_name=_('name'), max_length=30)
    service_id = models.UUIDField(verbose_name=_('service_id'), default=uuid.uuid4, editable=False)
    category = models.ManyToManyField(to='Category', verbose_name=_('categories'), related_name='service_category')
    price = MoneyField(verbose_name=_('price'), max_digits=15, decimal_places=0, default_currency='IRR')
    slug = models.SlugField(verbose_name=_('slug'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs) -> None:
        """Overriding 'save' method to fill 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class OrderService(models.Model):
    """model for Services ordered by customer"""
    order_uuid = models.UUIDField(verbose_name=_('order_uuid'), default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 verbose_name=_('customer'),
                                 blank=True,
                                 null=True)
    service = models.ManyToManyField(to='Service',
                                     verbose_name=_('services'),
                                     related_name='orderservice_service')
    content = models.TextField(verbose_name=_('contents (optional)'), blank=True)

    # These fields need to get changed and proccessed
    order_id = models.CharField(verbose_name=_('order id'), max_length=10, blank=True)
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
        return f'({self.id}){self.user.username}_order'
    
    def save(self, *args, **kwargs) -> None:
        """Overriding 'save' method to fill 'slug' field"""
        if not self.slug:
            self.slug = slugify(f'{self.user.username} order')
        super().save(*args, **kwargs)
