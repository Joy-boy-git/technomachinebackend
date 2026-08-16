from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Quotation
from .serializers import QuotationSerializer

from orders.models import Order


class QuotationViewSet(ModelViewSet):

    serializer_class = QuotationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    # ==========================================================
    # QUERYSET
    # ==========================================================

    def get_queryset(self):

        queryset = (
            Quotation.objects
            .select_related("created_by")
            .prefetch_related("items")
            .all()
        )

        # ======================================================
        # SEARCH
        # ======================================================

        search = self.request.query_params.get(
            "search"
        )

        if search:

            queryset = queryset.filter(
                Q(
                    quotation_number__icontains=search
                )
                |
                Q(
                    customer_name__icontains=search
                )
                |
                Q(
                    customer_phone__icontains=search
                )
                |
                Q(
                    customer_email__icontains=search
                )
            )

        # ======================================================
        # STATUS FILTER
        # ======================================================

        quotation_status = self.request.query_params.get(
            "status"
        )

        if quotation_status:

            queryset = queryset.filter(
                status=quotation_status
            )

        # ======================================================
        # YEAR FILTER
        # ======================================================

        year = self.request.query_params.get(
            "year"
        )

        if year:

            queryset = queryset.filter(
                quotation_date__year=year
            )

        # ======================================================
        # DATE FILTER
        # ======================================================

        date = self.request.query_params.get(
            "date"
        )

        if date:

            queryset = queryset.filter(
                quotation_date=date
            )

        return queryset

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        quotation = serializer.save(
            created_by=request.user
        )

        response_serializer = self.get_serializer(
            quotation
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        request,
        *args,
        **kwargs
    ):

        partial = kwargs.pop(
            "partial",
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        quotation = serializer.save()

        response_serializer = self.get_serializer(
            quotation
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def destroy(
        self,
        request,
        *args,
        **kwargs
    ):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "detail": "Quotation deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )

    # ==========================================================
    # CHANGE STATUS
    # ==========================================================

    def partial_update(
        self,
        request,
        *args,
        **kwargs
    ):

        instance = self.get_object()

        new_status = request.data.get(
            "status"
        )

        if new_status:

            valid_statuses = [
                choice[0]
                for choice
                in Quotation.STATUS_CHOICES
            ]

            if new_status not in valid_statuses:

                return Response(
                    {
                        "detail": (
                            "Invalid quotation status."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().partial_update(
            request,
            *args,
            **kwargs
        )

    # ==========================================================
    # CONVERT QUOTATION TO ORDER
    #
    # POST:
    #
    # /api/quotations/<id>/convert-to-order/
    #
    # ==========================================================

    @action(
        detail=True,
        methods=["post"],
        url_path="convert-to-order"
    )
    @transaction.atomic
    def convert_to_order(
        self,
        request,
        pk=None
    ):

        quotation = self.get_object()

        # ======================================================
        # PREVENT DUPLICATE CONVERSION
        # ======================================================

        if quotation.status == "Converted":

            return Response(
                {
                    "detail": (
                        "This quotation has already "
                        "been converted to an order."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ======================================================
        # GET QUOTATION ITEMS
        # ======================================================

        items = quotation.items.all()

        if not items.exists():

            return Response(
                {
                    "detail": (
                        "Cannot convert quotation "
                        "without any items."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ======================================================
        # GENERATE BASE ORDER NUMBER
        # ======================================================

        last_order = (
            Order.objects
            .order_by("-id")
            .first()
        )

        if last_order:

            try:

                last_number = int(
                    last_order.order_number
                    .replace("ORD-", "")
                )

                next_number = (
                    last_number + 1
                )

            except ValueError:

                next_number = (
                    last_order.id + 1
                )

        else:

            next_number = 1

        # ======================================================
        # CREATE ORDERS
        # ======================================================

        created_orders = []

        for index, item in enumerate(
            items,
            start=1
        ):

            # --------------------------------------------------
            # UNIQUE ORDER NUMBER
            # --------------------------------------------------

            order_number = (
                f"ORD-{next_number:05d}"
            )

            # Make sure it doesn't already exist
            while Order.objects.filter(
                order_number=order_number
            ).exists():

                next_number += 1

                order_number = (
                    f"ORD-{next_number:05d}"
                )

            # --------------------------------------------------
            # NOTES
            # --------------------------------------------------

            conversion_note = (
                f"Converted from quotation "
                f"{quotation.quotation_number}"
            )

            if item.description:

                conversion_note += (
                    f"\n\nItem description: "
                    f"{item.description}"
                )

            if quotation.notes:

                conversion_note += (
                    f"\n\nQuotation notes: "
                    f"{quotation.notes}"
                )

            # --------------------------------------------------
            # CREATE ORDER
            # --------------------------------------------------

            order = Order.objects.create(

                order_number=order_number,

                customer_name=(
                    quotation.customer_name
                ),

                customer_phone=(
                    quotation.customer_phone
                ),

                customer_email=(
                    quotation.customer_email
                ),

                order_date=(
                    quotation.quotation_date
                ),

                product_name=(
                    item.product_name
                ),

                quantity=int(
                    item.quantity
                ),

                amount=(
                    item.total
                ),

                status="Pending",

                notes=conversion_note,
            )

            created_orders.append(
                order
            )

            next_number += 1

        # ======================================================
        # MARK QUOTATION AS CONVERTED
        # ======================================================

        quotation.status = "Converted"

        quotation.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        # ======================================================
        # RESPONSE
        # ======================================================

        return Response(
            {
                "success": True,

                "message": (
                    "Quotation converted "
                    "to order successfully."
                ),

                "quotation_id": (
                    quotation.id
                ),

                "quotation_number": (
                    quotation.quotation_number
                ),

                "orders": [
                    {
                        "id": order.id,
                        "order_number": (
                            order.order_number
                        ),
                        "product_name": (
                            order.product_name
                        ),
                        "quantity": (
                            order.quantity
                        ),
                        "amount": (
                            str(order.amount)
                        ),
                        "status": (
                            order.status
                        ),
                    }
                    for order in created_orders
                ],
            },
            status=status.HTTP_201_CREATED
        )