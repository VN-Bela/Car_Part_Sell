from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from UserApp.models import User

# Create your models here.

user = get_user_model()
 

class CarPartCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100,null=True)
    year = models.PositiveIntegerField(default=2000)
    
    def __str__(self):
        return f"{self.manufacturer} {self.name} ({self.year})"
    

class CarPart(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(CarPartCategory, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images")

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart")
    purchase_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    is_paid=models.BooleanField(default=False)
    
    def get_cart_total(self):
     return sum(product.total_cost() for product in self.cart_products.all())

    

    def __str__(self):
        return f"{self.user} - {self.is_paid}"

class Cart_Product(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_products")
    car_part = models.ForeignKey(CarPart, on_delete=models.CASCADE,related_name="car_part")
    quantity = models.PositiveIntegerField(default=1)

    def total_cost(self):
        return self.car_part.price * self.quantity
    def get_cart_count(self):
        return self.cart.last().cart_products.all().count()
