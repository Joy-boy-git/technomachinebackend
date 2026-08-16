from django.db import models


class Document(models.Model):

    DOCUMENT_TYPES = [
        ("order", "Order"),
        ("quotation", "Quotation"),
        ("invoice", "Invoice"),
        ("service", "Service"),
        ("production", "Production"),
        ("customer", "Customer"),
        ("product", "Product"),
        ("other", "Other"),
    ]

    FILE_TYPES = [
        ("pdf", "PDF"),
        ("excel", "Excel"),
        ("word", "Word"),
        ("image", "Image"),
        ("other", "Other"),
    ]

    title = models.CharField(
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES,
        db_index=True,
    )

    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPES,
    )

    file = models.FileField(
        upload_to="historical_records/%Y/%m/"
    )

    document_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    customer_name = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    document_number = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    product_name = models.CharField(
        max_length=255,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    tags = models.CharField(
        max_length=500,
        blank=True,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-document_date",
            "-uploaded_at",
        ]

    def __str__(self):
        return self.title