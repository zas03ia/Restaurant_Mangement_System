from django.urls import path, include
from restaurant.rest.views.organization import PrivateOrganizationDetailView

urlpatterns = [
    path(
        "", PrivateOrganizationDetailView.as_view(), name="private-organization-detail"
    ),
]
