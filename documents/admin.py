from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "document_type",
        "file_type",
        "year",
        "customer_name",
        "product_name",
        "document_date",
        "uploaded_at",
    ]

    list_filter = [
        "document_type",
        "file_type",
        "year",
        "document_date",
    ]

    search_fields = [
        "title",
        "customer_name",
        "document_number",
        "product_name",
        "description",
        "tags",
    ]

    ordering = [
        "-document_date",
        "-uploaded_at",
    ]