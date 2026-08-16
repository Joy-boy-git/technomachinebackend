from django.db import transaction

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all().order_by("-created_at")

    serializer_class = OrderSerializer

    permission_classes = [
        IsAdminUser
    ]

    # =========================================================
    # CONFIRM ORDER
    # =========================================================

    @action(
        detail=True,
        methods=["patch"],
        url_path="confirm"
    )
    def confirm_order(
        self,
        request,
        pk=None
    ):

        order = self.get_object()

        # Only Pending orders can be confirmed
        if order.status != "Pending":

            return Response(
                {
                    "detail": (
                        f"Order is currently "
                        f"'{order.status}'. "
                        f"Only Pending orders "
                        f"can be confirmed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = "Confirmed"
        order.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )

    # =========================================================
    # START PRODUCTION
    # =========================================================

    @action(
        detail=True,
        methods=["post"],
        url_path="start-production"
    )
    @transaction.atomic
    def start_production(
        self,
        request,
        pk=None
    ):

        order = self.get_object()

        # -----------------------------------------------------
        # Order must be Confirmed
        # -----------------------------------------------------

        if order.status != "Confirmed":

            return Response(
                {
                    "detail": (
                        f"Order is currently "
                        f"'{order.status}'. "
                        f"Only Confirmed orders "
                        f"can start production."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------------------
        # Import here to avoid circular imports
        # -----------------------------------------------------

        from production.models import Production

        # -----------------------------------------------------
        # Check whether production already exists
        # -----------------------------------------------------

        if Production.objects.filter(
            order=order
        ).exists():

            return Response(
                {
                    "detail":
                        "Production has already been created for this order."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------------------
        # Generate Production Number
        # -----------------------------------------------------

        last_production = (
            Production.objects
            .order_by("-id")
            .first()
        )

        if last_production:

            next_id = (
                last_production.id + 1
            )

        else:

            next_id = 1

        production_number = (
            f"PRD-{next_id:04d}"
        )

        # -----------------------------------------------------
        # Create Production
        # -----------------------------------------------------

        production = Production.objects.create(

            production_number=
                production_number,

            order=order,

            product_name=
                order.product_name,

            quantity=
                order.quantity,

            conveyor_length=
                order.conveyor_length,

            conveyor_width=
                order.conveyor_width,

            motor_hp=
                order.motor_hp,

            status=
                "Pending",

            progress=
                0,

            notes=(
                f"Production created "
                f"from order {order.order_number}"
            )
        )

        # -----------------------------------------------------
        # Change Order Status
        # -----------------------------------------------------

        order.status = "Production"
        order.save()

        # -----------------------------------------------------
        # Return response
        # -----------------------------------------------------

        return Response(
            {
                "detail":
                    "Production started successfully.",

                "order": {
                    "id":
                        order.id,

                    "order_number":
                        order.order_number,

                    "status":
                        order.status,
                },

                "production": {
                    "id":
                        production.id,

                    "production_number":
                        production.production_number,

                    "status":
                        production.status,

                    "progress":
                        production.progress,
                }
            },
            status=status.HTTP_201_CREATED
        )