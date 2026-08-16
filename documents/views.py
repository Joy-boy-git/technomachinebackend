from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.db.models import Count

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Document
from .serializers import DocumentSerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def document_statistics(request):

    total = Document.objects.count()

    orders = Document.objects.filter(
        document_type="order"
    ).count()

    quotations = Document.objects.filter(
        document_type="quotation"
    ).count()

    invoices = Document.objects.filter(
        document_type="invoice"
    ).count()

    services = Document.objects.filter(
        document_type="service"
    ).count()

    production = Document.objects.filter(
        document_type="production"
    ).count()

    customers = Document.objects.filter(
        document_type="customer"
    ).count()

    products = Document.objects.filter(
        document_type="product"
    ).count()

    pdfs = Document.objects.filter(
        file_type="pdf"
    ).count()

    excel = Document.objects.filter(
        file_type="excel"
    ).count()

    word = Document.objects.filter(
        file_type="word"
    ).count()

    images = Document.objects.filter(
        file_type="image"
    ).count()

    recent_records = Document.objects.all()[:5]

    recent_data = []

    for document in recent_records:

        recent_data.append({
            "id": document.id,
            "title": document.title,
            "document_type": document.document_type,
            "file_type": document.file_type,
            "year": document.year,
            "document_date": document.document_date,
            "customer_name": document.customer_name,
            "product_name": document.product_name,
        })

    return Response({
        "total": total,

        "orders": orders,
        "quotations": quotations,
        "invoices": invoices,
        "services": services,
        "production": production,
        "customers": customers,
        "products": products,

        "pdfs": pdfs,
        "excel": excel,
        "word": word,
        "images": images,

        "recent_records": recent_data,
    })


class DocumentViewSet(viewsets.ModelViewSet):

    serializer_class = DocumentSerializer

    permission_classes = [
        IsAdminUser
    ]

    def get_queryset(self):

        queryset = Document.objects.all()

        params = self.request.query_params

        # General search
        search = params.get("search")

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(customer_name__icontains=search)
                | Q(document_number__icontains=search)
                | Q(product_name__icontains=search)
                | Q(description__icontains=search)
                | Q(tags__icontains=search)
            )

        # Document type
        document_type = params.get(
            "document_type"
        )

        if document_type:
            queryset = queryset.filter(
                document_type=document_type
            )

        # File type
        file_type = params.get(
            "file_type"
        )

        if file_type:
            queryset = queryset.filter(
                file_type=file_type
            )

        # Year
        year = params.get("year")

        if year:
            queryset = queryset.filter(
                year=year
            )

        # Exact date
        document_date = params.get(
            "document_date"
        )

        if document_date:
            queryset = queryset.filter(
                document_date=document_date
            )

        # Date from
        date_from = params.get(
            "date_from"
        )

        if date_from:
            queryset = queryset.filter(
                document_date__gte=date_from
            )

        # Date to
        date_to = params.get(
            "date_to"
        )

        if date_to:
            queryset = queryset.filter(
                document_date__lte=date_to
            )

        # Customer
        customer = params.get(
            "customer"
        )

        if customer:
            queryset = queryset.filter(
                customer_name__icontains=customer
            )

        # Product
        product = params.get(
            "product"
        )

        if product:
            queryset = queryset.filter(
                product_name__icontains=product
            )

        # Document number
        document_number = params.get(
            "document_number"
        )

        if document_number:
            queryset = queryset.filter(
                document_number__icontains=document_number
            )

        return queryset.order_by(
            "-document_date",
            "-uploaded_at"
        )