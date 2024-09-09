from django.urls import path, include

urlpatterns = [
    path("/menu", include("restaurant.rest.urls.menu")),
    path("/organization", include("restaurant.rest.urls.organization")),
]
