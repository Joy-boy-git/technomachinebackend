from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Production
from .serializers import ProductionSerializer


class ProductionViewSet(ModelViewSet):

    serializer_class = ProductionSerializer

    permission_classes = [
        IsAdminUser
    ]

    # =========================================================
    # QUERYSET
    # =========================================================

    def get_queryset(self):

        queryset = (
            Production.objects
            .select_related("order")
            .all()
            .order_by("-created_at")
        )

        # =====================================================
        # SEARCH
        # =====================================================

        search = self.request.query_params.get(
            "search"
        )

        if search:

            queryset = queryset.filter(
                Q(
                    production_number__icontains=search
                )
                |
                Q(
                    order__order_number__icontains=search
                )
                |
                Q(
                    order__customer_name__icontains=search
                )
                |
                Q(
                    product_name__icontains=search
                )
                |
                Q(
                    assigned_worker__icontains=search
                )
            )

        # =====================================================
        # STATUS FILTER
        # =====================================================

        production_status = (
            self.request.query_params.get(
                "status"
            )
        )

        if production_status:

            queryset = queryset.filter(
                status=production_status
            )

        return queryset

    # =========================================================
    # CREATE
    # =========================================================

    def perform_create(self, serializer):

        last_production = (
            Production.objects
            .order_by("-id")
            .first()
        )

        if last_production:
            next_id = last_production.id + 1
        else:
            next_id = 1

        production_number = (
            f"PRD-{next_id:04d}"
        )

        serializer.save(
            production_number=production_number
        )

    # =========================================================
    # UPDATE STATUS
    # =========================================================

    @action(
        detail=True,
        methods=["patch"],
        url_path="status"
    )
    def change_status(
        self,
        request,
        pk=None
    ):

        production = self.get_object()

        new_status = request.data.get(
            "status"
        )

        valid_statuses = [
            choice[0]
            for choice
            in Production.STATUS_CHOICES
        ]

        if new_status not in valid_statuses:

            return Response(
                {
                    "detail":
                        "Invalid production status."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        production.status = new_status

        # Automatically update progress
        if new_status == "Pending":
            production.progress = 0

        elif new_status == "In Production":

            if production.progress == 0:
                production.progress = 1

        elif new_status == "Completed":
            production.progress = 100

        elif new_status == "Cancelled":
            production.progress = 0

        production.save()

        return Response(
            ProductionSerializer(
                production
            ).data
        )

    # =========================================================
    # UPDATE PROGRESS
    # =========================================================

    @action(
        detail=True,
        methods=["patch"],
        url_path="progress"
    )
    def update_progress(
        self,
        request,
        pk=None
    ):

        production = self.get_object()

        progress = request.data.get(
            "progress"
        )

        if progress is None:

            return Response(
                {
                    "detail":
                        "Progress is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            progress = int(progress)

        except (TypeError, ValueError):

            return Response(
                {
                    "detail":
                        "Progress must be a number."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if progress < 0 or progress > 100:

            return Response(
                {
                    "detail":
                        "Progress must be between 0 and 100."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        production.progress = progress

        # Automatically determine status
        if progress == 0:

            production.status = "Pending"

        elif progress < 100:

            production.status = "In Production"

        else:

            production.status = "Completed"

        production.save()

        return Response(
            ProductionSerializer(
                production
            ).data
        )
        