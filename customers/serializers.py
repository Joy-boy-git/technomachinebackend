from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Customer

        fields = [
            "id",
            "customer_id",
            "username",
            "email",
            "full_name",
            "phone",
            "company_name",
            "address",
            "created_at",
            "updated_at",
        ]


class CustomerRegisterSerializer(serializers.Serializer):

    # --------------------------------------------------------
    # ACCOUNT DETAILS
    # --------------------------------------------------------

    username = serializers.CharField(
        max_length=150,
        trim_whitespace=True
    )

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    # --------------------------------------------------------
    # CUSTOMER DETAILS
    # --------------------------------------------------------

    full_name = serializers.CharField(
        max_length=200,
        trim_whitespace=True
    )

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True
    )

    company_name = serializers.CharField(
        max_length=200,
        required=True,
        trim_whitespace=True
    )

    address = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # --------------------------------------------------------
    # USERNAME VALIDATION
    # --------------------------------------------------------

    def validate_username(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Username is required."
            )

        if User.objects.filter(
            username__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    # --------------------------------------------------------
    # EMAIL VALIDATION
    # --------------------------------------------------------

    def validate_email(self, value):

        value = value.strip().lower()

        if User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    # --------------------------------------------------------
    # FULL NAME VALIDATION
    # --------------------------------------------------------

    def validate_full_name(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Full name is required."
            )

        return value

    # --------------------------------------------------------
    # COMPANY NAME VALIDATION
    # --------------------------------------------------------

    def validate_company_name(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Company name is required."
            )

        return value

    # --------------------------------------------------------
    # CREATE CUSTOMER ACCOUNT
    # --------------------------------------------------------

    @transaction.atomic
    def create(self, validated_data):

        # Create Django login account
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        # Generate customer ID automatically
        customer_id = f"CUST{user.id:05d}"

        # Create customer profile
        customer = Customer.objects.create(
            user=user,
            customer_id=customer_id,
            full_name=validated_data["full_name"],
            phone=validated_data.get(
                "phone",
                ""
            ),
            company_name=validated_data[
                "company_name"
            ],
            address=validated_data.get(
                "address",
                ""
            ),
        )

        return customer