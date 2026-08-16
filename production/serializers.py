from rest_framework import serializers

from .models import Production


class ProductionSerializer(serializers.ModelSerializer):

    # Show useful order information in the API
    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True
    )

    customer_name = serializers.CharField(
        source="order.customer_name",
        read_only=True
    )

    customer_phone = serializers.CharField(
        source="order.customer_phone",
        read_only=True
    )

    class Meta:
        model = Production

        fields = [
            "id",

            # Production
            "production_number",
            "status",
            "progress",

            # Order
            "order",
            "order_number",
            "customer_name",
            "customer_phone",

            # Product
            "product_name",
            "quantity",

            # Specifications
            "conveyor_length",
            "conveyor_width",
            "motor_hp",

            # Dates
            "start_date",
            "expected_completion_date",
            "actual_completion_date",

            # Production details
            "materials_required",
            "assigned_worker",
            "notes",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "production_number",
            "order_number",
            "customer_name",
            "customer_phone",
            "created_at",
            "updated_at",
        ]