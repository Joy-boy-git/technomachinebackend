from django.db import models
from orders.models import Order


class Production(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Production", "In Production"),
        ("On Hold", "On Hold"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    # =========================================================
    # PRODUCTION NUMBER
    # =========================================================

    production_number = models.CharField(
        max_length=100,
        unique=True
    )

    # =========================================================
    # CONNECTED ORDER
    # =========================================================

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="production"
    )

    # =========================================================
    # PRODUCT
    # =========================================================

    product_name = models.CharField(
        max_length=200,
        default="Belt Conveyor"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    # =========================================================
    # MACHINE SPECIFICATIONS
    # =========================================================

    conveyor_length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    conveyor_width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    motor_hp = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
    )

    # =========================================================
    # DATES
    # =========================================================

    start_date = models.DateField(
        blank=True,
        null=True
    )

    expected_completion_date = models.DateField(
        blank=True,
        null=True
    )

    actual_completion_date = models.DateField(
        blank=True,
        null=True
    )

    # =========================================================
    # PROGRESS
    # =========================================================

    progress = models.PositiveIntegerField(
        default=0
    )

    # =========================================================
    # STATUS
    # =========================================================

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    # =========================================================
    # MATERIALS
    # =========================================================

    materials_required = models.TextField(
        blank=True,
        null=True
    )

    # =========================================================
    # ASSIGNED WORKER
    # =========================================================

    assigned_worker = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    # =========================================================
    # NOTES
    # =========================================================

    notes = models.TextField(
        blank=True,
        null=True
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):
        return (
            f"{self.production_number} - "
            f"{self.product_name}"
        )