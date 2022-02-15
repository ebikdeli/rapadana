from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator


class MyUserManager(UserManager):
    """Create custom user manager for our custom User"""
    def create_user(self, username, password=None, name=None, **kwargs):
        if not username:
            raise ValueError('User must have a username')
        if 'email' in kwargs:
            email = self.normalize_email(kwargs['email'])
        else:
            email = None
        user = self.get_queryset().create(
            username=username,
            password=password,
            email=email
        )
        user.set_password(password)
        user.save()
        return user
    

class User(AbstractUser):
    username = models.CharField(verbose_name=_('user'), unique=True, help_text=_('username, email or phone number'), max_length=255)
    phone = models.CharField(max_length=13,
                             verbose_name=_('phone'),
                             validators=[MaxLengthValidator(13, _('phone number is too long')),
                                         MinLengthValidator(11, _('phone number length is too short'))],
                             blank=True,
                            )
    name = models.CharField(verbose_name=_('user name'),
                            max_length=50,
                            blank=True
                        )
    address = models.TextField(verbose_name=_('address'), blank=True)
    picture = models.ImageField(verbose_name=_('user picture'), blank=True)
    background = models.ImageField(verbose_name=_('profile background'), blank=True)
    score = models.IntegerField(verbose_name=_('user score'), default=0)
    score_lifetime = models.IntegerField(verbose_name=_('user life time score'), default=0)
    discount_value = models.DecimalField(verbose_name=_('user discount(value)'), default=0, max_digits=9,
                                         decimal_places=0)
    discount_percent = models.DecimalField(verbose_name=_('user discount(percent)'), default=0, max_digits=5,
                                           decimal_places=2,
                                           validators=[
                                               MaxValueValidator(100, _('percent could not be more than 100')),
                                               MinValueValidator(0, _('percent could not be less than 0'))
                                           ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = MyUserManager()
    

    def __str__(self) -> str:
        return self.username
