from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "product_code",
            "name",
            "category",
            "category_name",
            "short_description",
            "description",
            "belt_width",
            "conveyor_length",
            "motor_power",
            "speed",
            "load_capacity",
            "material",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        ]