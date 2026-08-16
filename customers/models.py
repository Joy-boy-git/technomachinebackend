from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    customer_id = models.CharField(
        max_length=50,
        unique=True
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.customer_id} - {self.full_name}"