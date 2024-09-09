from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from menu.models import Menu
from restaurant.rest.serializers.menu import PrivateMenuSerializer

from shared.utils import get_organization
from shared.permissions import IsOwnerAdminManager


class PrivateMenuListView(ListCreateAPIView):
    """
    Private Menu List
    """

    serializer_class = PrivateMenuSerializer
    permission_classes = [IsOwnerAdminManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ["name"]  # Search by name
    filterset_fields = ["name", "created_at"]  # Filter by name and created_at
    ordering_fields = ["name", "created_at"]  # Order by name and created_at

    def get_queryset(self):
        # Get organization base on domain name
        organization = get_organization(self.request)

        # Prefetch categories, items and their related modifiers
        menus = (
            Menu.objects.filter(organization=organization)
            .prefetch_related("categories__items__modifiers")
            .order_by("-created_at")
        )
        return menus


class PrivateMenuDetailView(RetrieveUpdateDestroyAPIView):
    """
    Private Menu Detail
    """

    serializer_class = PrivateMenuSerializer
    permission_classes = [IsOwnerAdminManager]

    def get_object(self):
        # Get organization base on domain name
        organization = get_organization(self.request)
        menu_uid = self.request.query_params.get("menu_uid")
        try:
            # Prefetch categories, items and their related modifiers
            menu = (
                Menu.objects.filter(organization=organization, uid=menu_uid)
                .prefetch_related("categories__items__modifiers")
                .first()
            )

            return menu
        except Menu.DoesNotExist:
            raise Exception("Provide a valid menu uid")
