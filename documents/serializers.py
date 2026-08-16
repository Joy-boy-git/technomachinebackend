from rest_framework import serializers

from .models import Document


class DocumentSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Document

        fields = [
            "id",
            "title",
            "document_type",
            "file_type",
            "file",
            "document_date",
            "year",
            "customer_name",
            "document_number",
            "product_name",
            "amount",
            "description",
            "tags",
            "uploaded_at",
            "updated_at",
        ]

        read_only_fields = [
            "uploaded_at",
            "updated_at",
        ]