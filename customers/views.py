from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer
from .serializers import (
    CustomerRegisterSerializer,
    CustomerSerializer,
)


# ============================================================
# CUSTOMER REGISTER
# ============================================================

class CustomerRegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = CustomerRegisterSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            customer = serializer.save()

            return Response(
                {
                    "message": "Customer account created successfully.",
                    "customer": CustomerSerializer(
                        customer
                    ).data,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            print(
                "CUSTOMER REGISTRATION ERROR:",
                str(e)
            )

            return Response(
                {
                    "detail": "Unable to create customer account.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================
# CUSTOMER LOGIN
# ============================================================

class CustomerLoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:

            return Response(
                {
                    "detail": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {
                    "detail": "Invalid username or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:

            customer = Customer.objects.get(
                user=user
            )

        except Customer.DoesNotExist:

            return Response(
                {
                    "detail": (
                        "This account is not registered "
                        "as a customer."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(
                    refresh.access_token
                ),

                "refresh": str(
                    refresh
                ),

                "user": CustomerSerializer(
                    customer
                ).data,
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# CUSTOMER PROFILE
# ============================================================

class CustomerProfileView(APIView):

    permission_classes = [IsAuthenticated]

    # --------------------------------------------------------
    # GET PROFILE
    # --------------------------------------------------------

    def get(self, request):

        try:

            customer = Customer.objects.get(
                user=request.user
            )

        except Customer.DoesNotExist:

            return Response(
                {
                    "detail": "Customer profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(
            customer
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # --------------------------------------------------------
    # UPDATE PROFILE
    # --------------------------------------------------------

    def patch(self, request):

        try:

            customer = Customer.objects.get(
                user=request.user
            )

        except Customer.DoesNotExist:

            return Response(
                {
                    "detail": "Customer profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(
            customer,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully.",
                "customer": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# CUSTOMER DETAILS
# ============================================================

class CustomerMeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            customer = Customer.objects.get(
                user=request.user
            )

        except Customer.DoesNotExist:

            return Response(
                {
                    "detail": "Customer profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            CustomerSerializer(
                customer
            ).data,
            status=status.HTTP_200_OK
        )