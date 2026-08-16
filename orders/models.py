from django.db import models


class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Production", "Production"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    order_number = models.CharField(
        max_length=100,
        unique=True
    )

    customer_name = models.CharField(
        max_length=200
    )

    customer_phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    customer_email = models.EmailField(
        blank=True,
        null=True
    )

    order_date = models.DateField()

    product_name = models.CharField(
        max_length=200,
        default="Belt Conveyor"
    )

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

    quantity = models.PositiveIntegerField(
        default=1
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.order_number} - {self.customer_name}"