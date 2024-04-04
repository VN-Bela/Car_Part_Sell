from django.contrib import admin

# Register your models here.
from .models import CarPartCategory,CarModel,CarPart,Cart,Cart_Product

# car model register
admin.site.register(CarPart)
admin.site.register(CarPartCategory)
admin.site.register(Cart)
admin.site.register(CarModel)
admin.site.register(Cart_Product)