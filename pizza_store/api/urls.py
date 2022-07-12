from django.urls import path, include

from rest_framework.routers import DefaultRouter

from pizza_store.api.views import PizzaViewSet, OrderViewSet, OrderItemViewSet
from .views import RegisterApi


router = DefaultRouter()
router.register("pizza", PizzaViewSet)
router.register("order", OrderViewSet)
router.register("orderitem", OrderItemViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterApi.as_view()),
]


urlpatterns += [
      path("auth/", include("rest_framework.urls")),
]
