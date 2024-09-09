from rest_framework import serializers
from core.models import User
from django.db import transaction
from accountio.models import Organization
from core.models import OrganizationUser
from restaurant.rest.serializers.organization import PrivateOrganizationDetailSerializer

from accountio.choices import OrganizationUserRoleChoices
from shared.utils import get_organization
from django.contrib.auth.hashers import make_password


class UserSerializer(
    serializers.ModelSerializer
):  # User serializer for registering new user
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data["password"]
        )  # Hash the password
        return super().create(validated_data)


class OrganizationOnboardingSerializer(
    PrivateOrganizationDetailSerializer
):  # For onboarding new organization
    class Meta:
        model = Organization
        fields = PrivateOrganizationDetailSerializer.Meta.fields
        read_only_fields = list(
            set(PrivateOrganizationDetailSerializer.Meta.read_only_fields)
            - {"domain", "name"}
        )

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]  # Access request from context

        try:
            # Create the organization
            organization = Organization.objects.create(**validated_data)

            # Add the owner of the organization
            OrganizationUser.objects.create(
                organization=organization,
                user=request.user,
                role=OrganizationUserRoleChoices.OWNER,
            )
        except Exception as e:  # raise exception
            raise serializers.ValidationError(f"Error creating organization: {str(e)}")

        return organization


class OrganizationUserOnboardingSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    user_role = serializers.ChoiceField(
        choices=OrganizationUserRoleChoices.choices, write_only=True
    )

    class Meta:
        model = OrganizationUser
        fields = ("email", "password", "user_role")

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]  # Access request from context

        # Get organization based on domain or any logic
        organization = get_organization(request)

        email = validated_data.get("email")
        password = validated_data.get("password")
        user_role = validated_data.get("user_role")

        try:
            # Create or fetch the user, ensuring password is hashed
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.password = make_password(password)  # Hash the password if new user
                user.save()

            # Create or get the OrganizationUser entry
            organization_user, created = OrganizationUser.objects.get_or_create(
                organization=organization,
                user=user,
                defaults={"role": user_role},
            )
            if not created:
                raise serializers.ValidationError(
                    f"User already exists with role '{organization_user.role}' in this organization."
                )

        except User.DoesNotExist:
            raise serializers.ValidationError("Failed to create or fetch user.")
        except Exception as e:
            raise serializers.ValidationError(f"Error onboarding user: {str(e)}")

        return organization
