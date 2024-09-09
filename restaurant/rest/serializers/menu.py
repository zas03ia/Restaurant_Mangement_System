from rest_framework import serializers
from menu.models import Menu, Item, Category, Modifier
from menu.rest.serializers.menu import (
    PublicModifierSerializer,
    PublicCategorySerializer,
    PublicItemSerializer,
    PublicMenuSerializer,
)


class PrivateModifierSerializer(PublicModifierSerializer):
    class Meta:
        model = Modifier
        fields = PublicModifierSerializer.Meta.fields + ["created_at", "updated_at"]
        read_only_fields = ["uid", "created_at", "updated_at"]


class PrivateItemSerializer(PublicItemSerializer):
    modifiers = PrivateModifierSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = PublicItemSerializer.Meta.fields + [
            "created_at",
            "updated_at",
            "quantity",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class PrivateCategorySerializer(PublicCategorySerializer):
    items = PrivateItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = PublicCategorySerializer.Meta.fields + ["created_at", "updated_at"]
        read_only_fields = ["uid", "created_at", "updated_at"]


class PrivateMenuSerializer(PublicMenuSerializer):
    categories = PrivateCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = PublicMenuSerializer.Meta.fields + ["created_at", "updated_at"]
        read_only_fields = ["uid", "created_at", "updated_at"]
