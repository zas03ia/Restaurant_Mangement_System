from rest_framework.generics import RetrieveUpdateAPIView
from restaurant.rest.serializers.organization import PrivateOrganizationDetailSerializer

from shared.utils import get_organization
from shared.permissions import IsOwner, IsOwnerAdminManager


class PrivateOrganizationDetailView(RetrieveUpdateAPIView):
    serializer_class = PrivateOrganizationDetailSerializer

    def get_permissions(self):
        """
        Return the permissions required for the request.
        """
        if self.request.method == "GET":
            # For GET requests, allow Owners, Admins, and Managers
            return [permission() for permission in [IsOwnerAdminManager]]
        # For non-GET requests (PUT, PATCH), allow only Owners
        return [permission() for permission in [IsOwner]]

    def get_object(self):
        """
        Return organization based on domain name
        """
        return get_organization(self.request)
