from django.conf import settings
from django.db import models

from versatileimagefield.fields import VersatileImageField

# Create your models here.


class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.user}"


class Adress(models.Model):
    name = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=30, blank=True)
    building = models.CharField(max_length=30, blank=True)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} for {self.client}"


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
        ClientProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    customer = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    accepted = models.BooleanField(auto_created=True, default=False)
    done = models.BooleanField(auto_created=True, default=False)
    order_list = models.ManyToManyField(Pizza, blank=True)
    
    def __str__(self):
        return f"Order {self.id} for {self.customer}"
