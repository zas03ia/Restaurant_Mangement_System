from django.urls import path, include

urlpatterns = [
    path("/oboarding", include("accountio.rest.urls.onboarding")),
    path("/auth", include("accountio.rest.urls.auth")),
    path("/organization", include("accountio.rest.urls.organization")),
]
