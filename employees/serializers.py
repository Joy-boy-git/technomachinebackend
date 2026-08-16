from rest_framework import serializers

from .models import (
    Employee,
    Attendance,
    LeaveApplication,
    EmployeeBonus,
    GatePass,
)


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


class LeaveApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveApplication
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "approved_by",
        ]


class EmployeeBonusSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeBonus
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "created_by",
        ]


class GatePassSerializer(serializers.ModelSerializer):

    class Meta:
        model = GatePass
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "approved_by",
        ]