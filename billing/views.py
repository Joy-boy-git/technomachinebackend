from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):

    queryset = Invoice.objects.prefetch_related(
        "items"
    ).select_related(
        "created_by"
    )

    serializer_class = InvoiceSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        invoice_number = self.request.query_params.get(
            "invoice_number"
        )

        customer_name = self.request.query_params.get(
            "customer_name"
        )

        payment_status = self.request.query_params.get(
            "payment_status"
        )

        year = self.request.query_params.get(
            "year"
        )

        if invoice_number:
            queryset = queryset.filter(
                invoice_number__icontains=invoice_number
            )

        if customer_name:
            queryset = queryset.filter(
                customer_name__icontains=customer_name
            )

        if payment_status:
            queryset = queryset.filter(
                payment_status=payment_status
            )

        if year:
            queryset = queryset.filter(
                invoice_date__year=year
            )

        return queryset