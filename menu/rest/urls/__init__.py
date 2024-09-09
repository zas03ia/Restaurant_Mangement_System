from django.urls import path, include

urlpatterns = [
    path("/menu", include("menu.rest.urls.menu")),
]
