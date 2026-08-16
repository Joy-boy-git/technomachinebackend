from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_name",
        "product_name",
        "quantity",
        "amount",
        "status",
        "order_date",
    )

    list_filter = (
        "status",
        "order_date",
        "product_name",
    )

    search_fields = (
        "order_number",
        "customer_name",
        "customer_phone",
        "customer_email",
    )

    ordering = (
        "-created_at",
    )