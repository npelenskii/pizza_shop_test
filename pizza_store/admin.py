from django.contrib import admin

from pizza_store.models import Pizza, Ingradient, Order, OrderItem
 
# Register your models here.

admin.site.register(Pizza)
admin.site.register(Ingradient)
admin.site.register(Order)
admin.site.register(OrderItem)