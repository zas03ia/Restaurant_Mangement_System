from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from accountio.rest.serializers.organization import PublicOrganizationDetailSerializer

from shared.utils import get_organization


class PublicOrganizationDetailView(RetrieveAPIView):
    """Public View"""

    serializer_class = PublicOrganizationDetailSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """
        Return organization based on domain name
        """
        return get_organization(self.request)
