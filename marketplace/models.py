from Tools.scripts.dutree import store
from django.db import models
from django.contrib.auth.models import User  # Reuse Django's built-in User model
from django.db.models import OneToOneField, CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vendor(models.Model):
    user=OneToOneField(User,on_delete=models.CASCADE)
    store_name=models.CharField(max_length=255)
    contact_info=models.TextField()
    def __str__(self):
        return self.store_name
class Product(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    description = models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=50,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'order {self.id} by {self.user.username}'
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=CASCADE)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
