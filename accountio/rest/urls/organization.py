from django.urls import path, include
from accountio.rest.views.organization import PublicOrganizationDetailView

urlpatterns = [
    path("", PublicOrganizationDetailView.as_view(), name="organization-detail"),
]
