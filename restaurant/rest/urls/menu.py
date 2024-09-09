from django.urls import path
from restaurant.rest.views.menu import PrivateMenuListView, PrivateMenuDetailView

urlpatterns = [
    path("", PrivateMenuListView.as_view(), name="private-menu-list"),
    path(
        "/<uuid:menu_uid>", PrivateMenuDetailView.as_view(), name="private-menu-detail"
    ),
]
