from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Quotation(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Sent", "Sent"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Expired", "Expired"),
        ("Converted", "Converted"),
    ]

    quotation_number = models.CharField(
        max_length=50,
        unique=True
    )

    quotation_date = models.DateField()

    valid_until = models.DateField(
        null=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=255
    )

    customer_phone = models.CharField(
        max_length=30,
        blank=True
    )

    customer_email = models.EmailField(
        blank=True
    )

    customer_address = models.TextField(
        blank=True
    )

    customer_gst = models.CharField(
        max_length=50,
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    gst_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    notes = models.TextField(
        blank=True
    )

    terms_conditions = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.quotation_number

    # ==========================================================
    # RECALCULATE TOTALS
    # ==========================================================

    def calculate_totals(self):

        subtotal = Decimal("0.00")
        gst_amount = Decimal("0.00")

        for item in self.items.all():

            subtotal += item.amount
            gst_amount += item.gst_amount

        discount = self.discount or Decimal("0.00")

        total = (
            subtotal
            - discount
            + gst_amount
        )

        self.subtotal = subtotal
        self.gst_amount = gst_amount
        self.total_amount = total

        self.save(
            update_fields=[
                "subtotal",
                "gst_amount",
                "total_amount",
                "updated_at",
            ]
        )


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        Quotation,
        related_name="items",
        on_delete=models.CASCADE
    )

    product_name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("1")
    )

    unit = models.CharField(
        max_length=30,
        default="Nos"
    )

    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    gst_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("18.00")
    )

    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00")
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    gst_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # ==========================================================
    # CALCULATE ITEM TOTAL
    # ==========================================================

    def calculate_totals(self):

        quantity = Decimal(
            str(self.quantity or 0)
        )

        unit_price = Decimal(
            str(self.unit_price or 0)
        )

        gst_percent = Decimal(
            str(self.gst_percent or 0)
        )

        discount_percent = Decimal(
            str(self.discount_percent or 0)
        )

        # Base amount
        base = (
            quantity *
            unit_price
        )

        # Item discount
        discount = (
            base *
            discount_percent /
            Decimal("100")
        )

        # Taxable amount
        taxable = (
            base -
            discount
        )

        # GST
        gst = (
            taxable *
            gst_percent /
            Decimal("100")
        )

        # Final total
        total = (
            taxable +
            gst
        )

        self.amount = taxable
        self.gst_amount = gst
        self.total = total

    def save(self, *args, **kwargs):

        self.calculate_totals()

        super().save(
            *args,
            **kwargs
        )

        # Recalculate quotation
        # after item is saved.

        if self.quotation_id:

            quotation = self.quotation

            subtotal = Decimal("0.00")
            gst_amount = Decimal("0.00")

            for item in quotation.items.all():

                subtotal += item.amount
                gst_amount += item.gst_amount

            discount = (
                quotation.discount or
                Decimal("0.00")
            )

            quotation.subtotal = subtotal

            quotation.gst_amount = gst_amount

            quotation.total_amount = (
                subtotal
                - discount
                + gst_amount
            )

            quotation.save(
                update_fields=[
                    "subtotal",
                    "gst_amount",
                    "total_amount",
                    "updated_at",
                ]
            )