from django.contrib import admin
from .models import Size, Product, Category, OrderedProduct, Customer, Ordered, OrderedProduct, Location, Topping


# Register your models here.
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderedProduct)
admin.site.register(Customer)
admin.site.register(Ordered)
admin.site.register(Location)
admin.site.register(Topping)
