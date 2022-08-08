from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField

# Create your models here.


class Ingradient(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(null=True, default=3)
    
    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=30)
    pizza_image = VersatileImageField(
        upload_to="pizza_images",
        null=True, 
        blank=True
    )
    ingradients = models.ManyToManyField(Ingradient, blank=True)
    ready_time = models.IntegerField(null=True, default=40)
    price_s = models.IntegerField(
        null=True,
        blank=True,
    )
    price_m = models.IntegerField(
        null=True,
        blank=True,
    )
    price_l = models.IntegerField(
        null=True,
        blank=True,
    )
    creater = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.name


class OrderItem(models.Model):
    pizza = models.ForeignKey(Pizza, blank=False, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, blank=False)
    
    def __str__(self):
        return F"{self.pizza.id}/{self.size}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=50, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(null=True, blank=True)
    order_list = models.ManyToManyField(OrderItem, blank=True)
    
    def __str__(self):
        return f"Order {self.id} for {self.customer}"
