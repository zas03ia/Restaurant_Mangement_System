from django.urls import path, include
from menu.rest.views.menu import PublicMenuListView

urlpatterns = [
    path("", PublicMenuListView.as_view(), name="organization-menus"),
]
