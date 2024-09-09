from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from menu.models import Menu
from menu.rest.serializers.menu import PublicMenuSerializer

from shared.utils import get_organization


class PublicMenuListView(ListAPIView):
    """
    Public Menu
    """

    serializer_class = PublicMenuSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Get organization base on domain name
        organization = get_organization(self.request)

        # Prefetch categories, items and their related modifiers
        menus = Menu.objects.filter(organization=organization).prefetch_related(
            "categories__items__modifiers"
        )
        return menus
