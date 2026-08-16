from decimal import Decimal

from rest_framework import serializers

from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem

        fields = [
            "id",
            "product_name",
            "description",
            "quantity",
            "unit_price",
            "discount_percent",
            "gst_percent",
            "amount",
        ]

        read_only_fields = [
            "id",
            "amount",
        ]


class InvoiceSerializer(serializers.ModelSerializer):

    items = InvoiceItemSerializer(
        many=True
    )

    class Meta:
        model = Invoice

        fields = [
            "id",
            "invoice_number",
            "invoice_date",
            "due_date",

            "customer_name",
            "customer_phone",
            "customer_email",
            "customer_address",
            "customer_gst",

            "payment_status",

            "subtotal",
            "discount",
            "taxable_amount",

            "gst_percent",
            "gst_amount",
            "grand_total",

            "notes",

            "created_by",
            "created_at",
            "updated_at",

            "items",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
            "subtotal",
            "taxable_amount",
            "gst_amount",
            "grand_total",
        ]

    def create(self, validated_data):

        items_data = validated_data.pop("items", [])

        invoice = Invoice.objects.create(
            created_by=self.context["request"].user,
            **validated_data,
        )

        subtotal = Decimal("0.00")

        for item_data in items_data:

            quantity = Decimal(
                item_data.get(
                    "quantity",
                    Decimal("1"),
                )
            )

            unit_price = Decimal(
                item_data.get(
                    "unit_price",
                    Decimal("0"),
                )
            )

            discount_percent = Decimal(
                item_data.get(
                    "discount_percent",
                    Decimal("0"),
                )
            )

            gst_percent = Decimal(
                item_data.get(
                    "gst_percent",
                    Decimal("0"),
                )
            )

            base_amount = quantity * unit_price

            discount_amount = (
                base_amount
                * discount_percent
                / Decimal("100")
            )

            taxable_item = (
                base_amount
                - discount_amount
            )

            gst_amount = (
                taxable_item
                * gst_percent
                / Decimal("100")
            )

            final_amount = (
                taxable_item
                + gst_amount
            )

            item_data["amount"] = final_amount

            InvoiceItem.objects.create(
                invoice=invoice,
                **item_data,
            )

            subtotal += base_amount

        discount = Decimal(
            validated_data.get(
                "discount",
                Decimal("0"),
            )
        )

        taxable_amount = subtotal - discount

        gst_percent = Decimal(
            validated_data.get(
                "gst_percent",
                Decimal("0"),
            )
        )

        gst_amount = (
            taxable_amount
            * gst_percent
            / Decimal("100")
        )

        grand_total = (
            taxable_amount
            + gst_amount
        )

        invoice.subtotal = subtotal
        invoice.taxable_amount = taxable_amount
        invoice.gst_amount = gst_amount
        invoice.grand_total = grand_total

        invoice.save(
            update_fields=[
                "subtotal",
                "taxable_amount",
                "gst_amount",
                "grand_total",
                "updated_at",
            ]
        )

        return invoice

    def update(self, instance, validated_data):

        items_data = validated_data.pop(
            "items",
            None,
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if items_data is not None:

            instance.items.all().delete()

            subtotal = Decimal("0.00")

            for item_data in items_data:

                quantity = Decimal(
                    item_data.get(
                        "quantity",
                        Decimal("1"),
                    )
                )

                unit_price = Decimal(
                    item_data.get(
                        "unit_price",
                        Decimal("0"),
                    )
                )

                discount_percent = Decimal(
                    item_data.get(
                        "discount_percent",
                        Decimal("0"),
                    )
                )

                gst_percent = Decimal(
                    item_data.get(
                        "gst_percent",
                        Decimal("0"),
                    )
                )

                base_amount = (
                    quantity * unit_price
                )

                discount_amount = (
                    base_amount
                    * discount_percent
                    / Decimal("100")
                )

                taxable_item = (
                    base_amount
                    - discount_amount
                )

                gst_amount = (
                    taxable_item
                    * gst_percent
                    / Decimal("100")
                )

                final_amount = (
                    taxable_item
                    + gst_amount
                )

                item_data["amount"] = final_amount

                InvoiceItem.objects.create(
                    invoice=instance,
                    **item_data,
                )

                subtotal += base_amount

            discount = instance.discount or Decimal("0")

            taxable_amount = (
                subtotal - discount
            )

            gst_percent = (
                instance.gst_percent
                or Decimal("0")
            )

            gst_amount = (
                taxable_amount
                * gst_percent
                / Decimal("100")
            )

            grand_total = (
                taxable_amount
                + gst_amount
            )

            instance.subtotal = subtotal
            instance.taxable_amount = taxable_amount
            instance.gst_amount = gst_amount
            instance.grand_total = grand_total

            instance.save()

        return instance