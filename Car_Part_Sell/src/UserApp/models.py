from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

# Buyer and seller Model
class User(AbstractUser):
    SELLER = 0
    BUYER = 1
    USER_TYPE = ((SELLER, "Seller"), (BUYER, "Buyer"))

    user_role = models.IntegerField(choices=USER_TYPE, default=BUYER)
    email = models.EmailField(_("email address"), unique=True)
    mobile = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # url Redirect
    def get_absolute_url(self):
        return "/login/"
    
    def get_cart_count(self):
        return self.cart.last().cart_products.all().count()
