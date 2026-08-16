from django.contrib import admin

from .models import Invoice, InvoiceItem


class InvoiceItemInline(
    admin.TabularInline
):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "customer_name",
        "invoice_date",
        "payment_status",
        "grand_total",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "invoice_date",
    )

    search_fields = (
        "invoice_number",
        "customer_name",
        "customer_phone",
        "customer_email",
        "customer_gst",
    )

    readonly_fields = (
        "subtotal",
        "taxable_amount",
        "gst_amount",
        "grand_total",
        "created_at",
        "updated_at",
    )

    inlines = [
        InvoiceItemInline
    ]