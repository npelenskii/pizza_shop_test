from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from pizza_store.models import ClientProfile, Pizza, Adress, Ingradient, Order




class IngradientField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(name=data.lower())[0]
        except (TypeError, ValueError):
            self.fail(f"Ingradient value {data} is invalid")


class PizzaSerializer(serializers.ModelSerializer):

    ingradients = IngradientField(
        slug_field="name", many=True, queryset=Ingradient.objects.all()
    )
    pizza_image = VersatileImageFieldSerializer(
        sizes=[
            ("full_size", "url"),
            ("thumbnail", "thumbnail__150x150"),
        ],
        read_only=True,
    )
    
    class Meta:
        model = Pizza
        fields = "__all__"
        
