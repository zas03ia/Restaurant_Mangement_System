from django.urls import path, include
from accountio.rest.views.onboarding import (
    UserRegistrationView,
    OrganizationOnboardingView,
    OrganizationUserOnboardingView,
)

urlpatterns = [
    path("/user", UserRegistrationView.as_view(), name="onboarding-user"),
    path(
        "/organization",
        OrganizationOnboardingView.as_view(),
        name="onboarding-organization",
    ),
    path(
        "/organization-user",
        OrganizationUserOnboardingView.as_view(),
        name="onboarding-organization-user",
    ),
]
