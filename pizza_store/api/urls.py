from django.urls import path, include, re_path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from pizza_store.api.views import PizzaViewSet


router = DefaultRouter()
router.register("pizza", PizzaViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


urlpatterns += [
      path("auth/", include("rest_framework.urls")),
]
