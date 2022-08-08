from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.views import TokenObtainPairView

from pizza_store.models import OrderItem, Pizza, Order
from .serializers import RegisterSerializer, UserSerializer, OrderSerializer, OrderCreateSerializer, OrderItemSerializer, OrderItemCreateSerializer, PizzaSerializer, MyTokenObtainPairSerializer
from pizza_images.pizza_image import ImageCreator


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied("You can't create pizza, if not authenticated")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        self.request.data.get("ingradients", None) 
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        pizza_image = str(self.get_object().pizza_image)
        result = ImageCreator.delete_pizza_image(path=pizza_image)
        print(result)
        
        return super().destroy(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderItemCreateSerializer
        return OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ("create"):
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not request.user.is_anonymous:
            for item in serializer.validated_data['order_list']:
                order_item = OrderItem.objects.get(id=item)
                pizza_creater = Pizza.objects.get(name=order_item.pizza.name).creater
                if pizza_creater != None and pizza_creater != request.user:
                    raise PermissionDenied("You can't add Pizza that was created by another person")
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(methods=["get"], detail=False, name="Orders by user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Orders are yours")
        orders = self.get_queryset().filter(customer=request.user)
        
        serializer = OrderSerializer(orders, many=True, context={"request": request})
        
        if (len(serializer.data) > 0):
            return Response(serializer.data)
        else:
            return Response({
                "detail": "You have no Orders"
            })


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(
                user,
                context=self.get_serializer_context()
            ).data,
        })
