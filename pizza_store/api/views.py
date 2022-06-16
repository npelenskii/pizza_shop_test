from rest_framework import generics, viewsets

from pizza_store.api.serializers import PizzaSerializer
from pizza_store.models import ClientProfile, Pizza, Adress, Ingradient, Order

class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    
    
    