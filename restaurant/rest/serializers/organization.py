from rest_framework import serializers
from accountio.models import Organization, Location
from accountio.rest.serializers.organization import (
    PublicLocationSlimSerializer,
    PublicOrganizationDetailSerializer,
)


class PrivateLocationSlimSerializer(PublicLocationSlimSerializer):
    class Meta:
        model = Location
        # Extend the fields from PublicLocationSlimSerializer
        fields = PublicLocationSlimSerializer.Meta.fields + (
            "uid",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "uid",
            "created_at",
            "updated_at",
        )


class PrivateOrganizationDetailSerializer(PublicOrganizationDetailSerializer):
    locations = PrivateLocationSlimSerializer(many=True)

    class Meta:
        model = Organization
        # Extend the fields from PublicOrganizationDetailSerializer
        fields = PublicOrganizationDetailSerializer.Meta.fields + (
            "uid",
            "created_at",
            "updated_at",
            "domain",
        )
        read_only_fields = ("uid", "created_at", "updated_at", "domain", "name")
