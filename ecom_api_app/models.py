from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class CustomManager(models.Manager):
    pass

UserRole_CHOICES = (
    ("customer", "Customer"),
    ("Vendor", "Vendor"),
)


class UserRole(models.Model):
    title = models.CharField(
        max_length=20,
        choices=UserRole_CHOICES,
        default='customer'
    )

    def __str__(self):
        return self.title


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError({'details': 'Email cant be empty...'})

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    userrole = models.ForeignKey(
        'ecom_api_app.UserRole', on_delete=models.CASCADE, null=True, related_name='user')

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

class ProductName(models.Model):
    vender = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='product')
    product_name = models.CharField(max_length=56)
    price = models.FloatField()

    def __str__(self):
        return self.product_name


Order_CHOICES = (
    ("Placed", "Order Placed"),
    ("Accepted", "Order Accepted"),
    ("Cancelled", "Order Cancelled"),
)


class Order(models.Model):
    order_item = models.OneToOneField(
        'OrderItem', on_delete=models.CASCADE, null=True, related_name='order')
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, null=False, related_name='order_user')
    vender = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, null=False, related_name='order_vender')
    order_status = models.CharField(
        max_length=20,
        choices=Order_CHOICES,
        default='Placed'
    )

    def __str__(self):
        return self.user.first_name


class OrderItem(models.Model):
    productname = models.ForeignKey(
        "ProductName", on_delete=models.CASCADE, related_name='order_item')
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.productname.product_name
