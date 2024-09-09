from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from accountio.rest.serializers.onboarding import (
    UserSerializer,
    OrganizationOnboardingSerializer,
    OrganizationUserOnboardingSerializer,
)
from shared.permissions import IsOwnerAdmin


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class OrganizationOnboardingView(CreateAPIView):
    serializer_class = OrganizationOnboardingSerializer
    permission_classes = [IsAuthenticated]


class OrganizationUserOnboardingView(CreateAPIView):
    serializer_class = OrganizationUserOnboardingSerializer
    permission_classes = [IsOwnerAdmin]
