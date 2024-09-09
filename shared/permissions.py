from rest_framework.permissions import BasePermission
from .utils import get_organization
from core.models import OrganizationUser
from accountio.choices import OrganizationUserRoleChoices


# Custom base permission class
class BaseOrganizationUserPermission(BasePermission):
    def get_organization_user(self, request):
        # check for authorization
        if not request.user.is_authenticated:
            return None
        organization = get_organization(request)
        try:
            # check if current user is organization member
            return OrganizationUser.objects.filter(
                user=request.user, organization=organization
            ).first()
        except OrganizationUser.DoesNotExist:
            return None

    def has_object_permission(self, request, view, obj):
        organization_user = self.get_organization_user(request)
        if organization_user is None:
            return False
        return self.check_role(organization_user)  # check for user role

    def check_role(self, organization_user):  # base check is prevented
        raise NotImplementedError("Subclasses must implement this method")


class IsOwner(BaseOrganizationUserPermission):
    def check_role(self, organization_user):
        return organization_user.role == OrganizationUserRoleChoices.OWNER


class IsOwnerAdmin(BaseOrganizationUserPermission):
    def check_role(self, organization_user):
        return organization_user.role in [
            OrganizationUserRoleChoices.OWNER,
            OrganizationUserRoleChoices.ADMIN,
        ]


class IsOwnerAdminManager(BaseOrganizationUserPermission):
    def check_role(self, organization_user):
        return organization_user.role in [
            OrganizationUserRoleChoices.OWNER,
            OrganizationUserRoleChoices.MANAGER,
            OrganizationUserRoleChoices.ADMIN,
        ]


class IsRestaurantStaff(BaseOrganizationUserPermission):
    def check_role(self, organization_user):
        return organization_user.role in [
            OrganizationUserRoleChoices.OWNER,
            OrganizationUserRoleChoices.ADMIN,
            OrganizationUserRoleChoices.MANAGER,
            OrganizationUserRoleChoices.RIDER,
        ]
