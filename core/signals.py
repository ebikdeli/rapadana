from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='core.Customer')
def slug_customer(sender, instance, created, **kwargs):
    """Fill 'slug' field in Customer model"""
    if not instance.slug:
        if instance.name:
            instance.slug = instance.name


@receiver(post_save, sender='core.Order')
def slug_order(sender, instance, created, **kwargs):
    """Fill 'slug' field in Order model"""
    if not instance.slug:
        if instance.customer:
            current_customer = instance.customer
            if current_customer.name:
                instance.slug = f'{current_customer.name}_order'


@receiver(post_save, sender='core.Order')
def generate_order_id(sender, instance, created, **kwargs):
    """Generate random id for any order would be created by admin"""
    if created:
        instance.order_id = generate_order_id()


def generate_random_id(length=10):
    """To create random number for 'Order's 'order_id' field"""
    # 'length' is the numbers of charcters in the string
    import random
    import string
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return ran