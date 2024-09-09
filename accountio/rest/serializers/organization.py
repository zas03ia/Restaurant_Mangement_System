from rest_framework import serializers
from accountio.models import Organization, Location


class PublicLocationSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("name", "address", "city", "state", "postal_code", "country")
        read_only_fields = fields


class PublicOrganizationDetailSerializer(
    serializers.ModelSerializer
):  # organization for public view
    locations = PublicLocationSlimSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = (
            "name",
            "description",
            "vat",
            "locations",
            "start_week_day",
            "end_week_day",
            "start_time",
            "end_time",
        )
        read_only_fields = fields
