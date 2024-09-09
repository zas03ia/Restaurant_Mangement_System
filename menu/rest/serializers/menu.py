from rest_framework import serializers
from menu.models import Menu, Item, Category, Modifier


class PublicModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modifier
        fields = ["uid", "name", "price"]
        read_only_fields = fields


class PublicItemSerializer(serializers.ModelSerializer):
    modifiers = PublicModifierSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "uid",
            "name",
            "description",
            "price",
            "available",
            "modifiers",
        ]
        read_only_fields = fields


class PublicCategorySerializer(serializers.ModelSerializer):
    items = PublicItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["uid", "name", "items"]
        read_only_fields = fields


class PublicMenuSerializer(serializers.ModelSerializer):
    categories = PublicCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ["uid", "name", "description", "categories"]
        read_only_fields = fields
