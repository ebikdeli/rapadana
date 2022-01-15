from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(post_save, sender='core.Customer')
def slug_customer(sender, instance, created, **kwargs):
    """Fill 'slug' field in Customer model"""
    if created:
        if instance.name:
            instance.slug = instance.name
    if instance.name:
        instance.slug = instance.name


@receiver(post_save, sender='core.Order')
def slug_order(sender, instance, created, **kwargs):
    """Fill 'slug' field in Order model"""
    if instance.customer.exists():
        current_customer = instance.customer.first()
        if created:
            if current_customer.name:
                instance.slug = f'{current_customer.name}_order'
        if current_customer.name:
            instance.slug = f'{current_customer.name}_order'


@receiver(post_save, sender='core.Order')
def generate_order_id(sender, created, instance, **kwargs):
    """Generate random id for any order would be created by admin"""
    if created:
        instance.order_id = generate_order_id()


def generate_random_id():
    """To create random number for 'Order's 'order_id' field"""
    import random
    import string
    s = 10  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=s))
    return ran