from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(pre_save, sender='core.Customer')
def slug_customer(sender, instance, **kwargs):
    """Fill 'slug' field in Customer model"""
    if not instance.slug:
        if instance.name:
            instance.slug = instance.name


@receiver(post_save, sender='core.Order')
def count_remain_price(sender, instance, created, **kwargs):
    """Count remain price after creating new Order"""
    if created:
        instance.remain = instance.price
        instance.save()
    if instance.price and instance.remain < 0:
        instance.remain = instance.price
        instance.save()


@receiver(pre_save, sender='core.Order')
def slug_order(sender, instance, **kwargs):
    """Fill 'slug' field in Order model"""
    if not instance.slug:
        if instance.customer:
            current_customer = instance.customer
            if current_customer.name:
                instance.slug = f'{current_customer.name}_order'


@receiver(pre_save, sender='core.Order')
def generate_order_id(sender, instance, **kwargs):
    """Generate random id for any order would be created by admin"""
    if not instance.order_id:
        instance.order_id = generate_random_id()


def generate_random_id(length=10):
    """To create random number for 'Order's 'order_id' field"""
    # 'length' is the numbers of charcters in the string
    import random
    import string
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return ran