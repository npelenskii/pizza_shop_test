from django.contrib import admin

from pizza_store.models import ClientProfile, Pizza, Adress, Ingradient, Order
 
# Register your models here.

admin.site.register(ClientProfile)
admin.site.register(Pizza)
admin.site.register(Adress)
admin.site.register(Ingradient)
admin.site.register(Order)