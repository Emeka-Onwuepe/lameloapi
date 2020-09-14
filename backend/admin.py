from django.contrib import admin
from .models import Size, Product, Category, OrderedProduct, Customer, Order


# Register your models here.
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderedProduct)
admin.site.register(Customer)
admin.site.register(Order)
