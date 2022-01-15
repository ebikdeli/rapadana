"""
Important: If we want to use the 'username' field to authenticate users, we must not use 'AbstractBaseUser' model otherwise we
get errors. To use 'username' field we should inherent from 'AbstractUser' model and we don't have to define custom user manager
from scratch. And because 'AbstractUser' model by default inherent from 'PermissionMixin' we should not use the latter.
https://stackoverflow.com/questions/46093946/django-1-10-custom-user-is-superuser-clashes-with-the-field-is-superuser-fro
"""
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator


class MyUserManager(UserManager):
    """Create custom user manager for our custom User"""
    def create_user(self, username, password=None, name=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('User must have a username')

        # actually below line is this <==> user = User(email=User.objects.normalize_email(email), password=password)
        # This is how we can use 'kwargs' in methods or functions
        if 'email' in kwargs:
            email = self.normalize_email(kwargs['email'])
        else:
            email = None
        # user = self.model(    <==> This line could only be used for AbstractBaseUser
        #     username,
        #     password
        # )
        user = self.get_queryset().create(
            username=username,
            password=password,
            email=email
        )
        user.set_password(password)
        # user.save(using=self._db)     <==> This line could only be used for AbstractBaseUser
        user.save()
        return user
    
    #def create_superuser(self, username, password=None, name=None, **kwargs):
    #    """
    #    Creates and saves a superuser with the given email and password.
    #    """
    #    user = self.create_user(
    #        username,
    #        password,
    #        name,
    #    )
    #    user.is_staff = True
    #    user.is_admin = True
    #    user.is_superuser = True
    #    user.save(using=self._db)
    #    return user


class User(AbstractUser):
    username = models.CharField(verbose_name=_('user'), unique=True, help_text=_('username, email or phone number'), max_length=255)
    # Stupid fucking django below link:
    # https://stackoverflow.com/questions/17257031/django-unique-null-and-blank-charfield-giving-already-exists-error-on-admin-p
    phone = models.CharField(max_length=13,
                             verbose_name=_('phone'),
                             validators=[MaxLengthValidator(13, _('phone number is too long')),
                                         MinLengthValidator(11, _('phone number length is too short'))],
                             blank=True,
                             null=True
                            )
    email = models.EmailField(verbose_name=_('email'), null=True, blank=True)
    name = models.CharField(verbose_name=_('name'),
                            max_length=50,
                            blank=True,
                            null=True)
    address = models.TextField(verbose_name=_('address'), null=True, blank=True)
    picture = models.ImageField(verbose_name=_('user picture'), blank=True, null=True)
    background = models.ImageField(verbose_name=_('profile background'), blank=True, null=True)
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
    
    def get_absolute_url(self):
        # return reverse("model_detail", kwargs={"pk": self.pk, "slug": self.slug})
        # OR
        # return reverse('model_detail', self.pk, self.slug))
        pass
