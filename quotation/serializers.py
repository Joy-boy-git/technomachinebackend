from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import Quotation, QuotationItem


class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = [
            "id",
            "product_name",
            "description",
            "quantity",
            "unit",
            "unit_price",
            "gst_percent",
            "discount_percent",
            "amount",
            "gst_amount",
            "total",
        ]

        read_only_fields = [
            "id",
            "amount",
            "gst_amount",
            "total",
        ]


class QuotationSerializer(serializers.ModelSerializer):

    items = QuotationItemSerializer(
        many=True
    )

    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    class Meta:
        model = Quotation

        fields = [
            "id",
            "quotation_number",
            "quotation_date",
            "valid_until",

            "customer_name",
            "customer_phone",
            "customer_email",
            "customer_address",
            "customer_gst",

            "subtotal",
            "discount",
            "gst_amount",
            "total_amount",

            "notes",
            "terms_conditions",

            "status",

            "created_by",
            "created_by_username",

            "created_at",
            "updated_at",

            "items",
        ]

        read_only_fields = [
            "id",
            "subtotal",
            "gst_amount",
            "total_amount",
            "created_by",
            "created_by_username",
            "created_at",
            "updated_at",
        ]

    # ==========================================================
    # CALCULATE QUOTATION TOTALS
    # ==========================================================

    def calculate_quotation_totals(self, quotation):

        subtotal = Decimal("0.00")
        gst_amount = Decimal("0.00")

        for item in quotation.items.all():

            subtotal += Decimal(str(item.amount))
            gst_amount += Decimal(str(item.gst_amount))

        discount = Decimal(
            str(quotation.discount or 0)
        )

        total_amount = (
            subtotal
            - discount
            + gst_amount
        )

        quotation.subtotal = subtotal
        quotation.gst_amount = gst_amount
        quotation.total_amount = total_amount

        quotation.save(
            update_fields=[
                "subtotal",
                "gst_amount",
                "total_amount",
                "updated_at",
            ]
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    @transaction.atomic
    def create(self, validated_data):

        items_data = validated_data.pop(
            "items",
            []
        )

        request = self.context.get(
            "request"
        )

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        quotation = Quotation.objects.create(
            **validated_data
        )

        for item_data in items_data:

            QuotationItem.objects.create(
                quotation=quotation,
                **item_data
            )

        self.calculate_quotation_totals(
            quotation
        )

        return quotation

    # ==========================================================
    # UPDATE
    # ==========================================================

    @transaction.atomic
    def update(
        self,
        instance,
        validated_data
    ):

        items_data = validated_data.pop(
            "items",
            None
        )

        # ------------------------------------------------------
        # UPDATE QUOTATION FIELDS
        # ------------------------------------------------------

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        # ------------------------------------------------------
        # UPDATE ITEMS
        # ------------------------------------------------------

        if items_data is not None:

            # Delete old items
            instance.items.all().delete()

            # Create new items
            for item_data in items_data:

                QuotationItem.objects.create(
                    quotation=instance,
                    **item_data
                )

        # ------------------------------------------------------
        # RECALCULATE TOTALS
        # ------------------------------------------------------

        self.calculate_quotation_totals(
            instance
        )

        return instance