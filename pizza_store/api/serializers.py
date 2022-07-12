from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from pizza_images.pizza_image import ImageCreator
import string
import random
from rest_framework import  serializers
from django.contrib.auth.models import User

from pizza_store.models import Pizza, Ingradient, Order, OrderItem


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


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
    
    def create(self, validated_data):
        
        image = ImageCreator(validated_data["ingradients"])
        image_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        image.create_pizza_image(image_name)
        
        price = 0
        for ing in validated_data["ingradients"]:
            price += 2
        
        pizza = Pizza.objects.create(
            name = validated_data["name"], 
            price_s = 5 + price,
            price_m = 8 + price, 
            price_l = 11 + price,  
            ready_time = validated_data["ready_time"], 
            creater = validated_data["creater"],
            pizza_image = (f"pizza_images/{image_name}.png")
        )
        pizza.ingradients.set(validated_data["ingradients"])
        
        return pizza


class PizzaField(serializers.StringRelatedField):
    
    def to_internal_value(self, data):
        try:
            print(data)
            return self.get_queryset().get_or_create(name=data.lower())[0]
        except (TypeError, ValueError):
            self.fail(f"Pizza value {data} is invalid")


class OrderItemSerializer(serializers.ModelSerializer):
    
    pizza = serializers.SlugRelatedField(slug_field="name", many=False, queryset=Pizza.objects.all())
    
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderItemField(serializers.StringRelatedField):

    def to_internal_value(self, data):
        try:
            order_item = data.split("/")
            pizza = Pizza.objects.get(name=order_item[0])
            orderItem = OrderItem.objects.get_or_create(pizza=pizza, size=order_item[1])[0]
            return orderItem.id
        except (TypeError):
            self.fail(f"Order item value {data} is invalid")


class OrderSerializer(serializers.ModelSerializer):
    
    order_list = OrderItemField(many=True)
    
    class Meta:
        model = Order
        fields = "__all__"
    
    def create(self, validated_data):
        
        order_list_original = validated_data.pop("order_list")
        
        price = 0
        for item in order_list_original:
            order_item = OrderItem.objects.get(id=item) 
            pizza = Pizza.objects.get(name=order_item.pizza.name)
            
            if order_item.size == "S":
                price += pizza.price_s
            elif order_item.size == "M":
                price += pizza.price_m
            else:
                price += pizza.price_l
        
        order = Order.objects.create(**validated_data)
        order.price = price
        order.order_list.set(order_list_original)
        
        return order


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],     
            password = validated_data['password'],
            first_name=validated_data['first_name'],  
            last_name=validated_data['last_name']
        )
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
