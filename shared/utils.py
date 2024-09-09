from accountio.models import Organization
from rest_framework.exceptions import ValidationError
from django.http import Http404


def get_organization(request):
    # fetch organization domain from domain header
    domain = request.headers.get("X-DOMAIN", None)
    try:
        # retrieve organization based on domain
        organization = Organization.objects.get(domain=domain.title())
        return organization
    except Organization.DoesNotExist:
        raise Http404("Organization not found")
