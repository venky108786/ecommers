from django.contrib import admin

# Register your models here.
from .models import Vendor, Product, Order, OrderItem, Review
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)