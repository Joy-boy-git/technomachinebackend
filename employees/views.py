from django.db.models import Sum
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Employee,
    Attendance,
    LeaveApplication,
    EmployeeBonus,
    GatePass,
)

from .serializers import (
    EmployeeSerializer,
    AttendanceSerializer,
    LeaveApplicationSerializer,
    EmployeeBonusSerializer,
    GatePassSerializer,
)


# ============================================================
# Employee ViewSet
# ============================================================

class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all().order_by("-id")

    serializer_class = EmployeeSerializer

    permission_classes = [
        IsAuthenticated
    ]
    # --------------------------------------------------------
    # FILTERING / SEARCH
    # --------------------------------------------------------

    def get_queryset(self):

        queryset = Employee.objects.all()

        search = self.request.query_params.get(
            "search"
        )

        department = self.request.query_params.get(
            "department"
        )

        employee_status = self.request.query_params.get(
            "status"
        )

        if search:

            queryset = queryset.filter(
                full_name__icontains=search
            ) | queryset.filter(
                employee_id__icontains=search
            ) | queryset.filter(
                phone__icontains=search
            )

        if department:

            queryset = queryset.filter(
                department__iexact=department
            )

        if employee_status:

            queryset = queryset.filter(
                status=employee_status
            )

        return queryset.order_by(
            "-id"
        )

    # --------------------------------------------------------
    # EMPLOYEE DETAILS
    # --------------------------------------------------------

    @action(
        detail=True,
        methods=["get"],
        url_path="details"
    )
    def details(self, request, pk=None):

        employee = self.get_object()

        serializer = self.get_serializer(
            employee
        )

        return Response(
            serializer.data
        )

    # --------------------------------------------------------
    # EMPLOYEE STATISTICS
    # --------------------------------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="statistics"
    )
    def statistics(self, request):

        total = Employee.objects.count()

        active = Employee.objects.filter(
            status="Active"
        ).count()

        inactive = Employee.objects.filter(
            status="Inactive"
        ).count()

        resigned = Employee.objects.filter(
            status="Resigned"
        ).count()

        terminated = Employee.objects.filter(
            status="Terminated"
        ).count()

        departments = (
            Employee.objects
            .values("department")
            .annotate(total=Sum("id"))
        )

        return Response({
            "total": total,
            "active": active,
            "inactive": inactive,
            "resigned": resigned,
            "terminated": terminated,
        })

    # --------------------------------------------------------
    # ACTIVE EMPLOYEES
    # --------------------------------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="active"
    )
    def active(self, request):

        employees = Employee.objects.filter(
            status="Active"
        ).order_by("full_name")

        serializer = self.get_serializer(
            employees,
            many=True
        )

        return Response(
            serializer.data
        )


# ============================================================
# ATTENDANCE VIEWSET
# ============================================================

class AttendanceViewSet(viewsets.ModelViewSet):

    queryset = Attendance.objects.select_related(
        "employee"
    ).all()

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = self.queryset

        employee = self.request.query_params.get(
            "employee"
        )

        date = self.request.query_params.get(
            "date"
        )

        month = self.request.query_params.get(
            "month"
        )

        year = self.request.query_params.get(
            "year"
        )

        attendance_status = (
            self.request.query_params.get(
                "status"
            )
        )

        if employee:

            queryset = queryset.filter(
                employee_id=employee
            )

        if date:

            queryset = queryset.filter(
                date=date
            )

        if month:

            queryset = queryset.filter(
                date__month=month
            )

        if year:

            queryset = queryset.filter(
                date__year=year
            )

        if attendance_status:

            queryset = queryset.filter(
                status=attendance_status
            )

        return queryset.order_by(
            "-date"
        )

    # --------------------------------------------------------
    # MONTHLY SUMMARY
    # --------------------------------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="monthly-summary"
    )
    def monthly_summary(self, request):

        employee_id = request.query_params.get(
            "employee"
        )

        month = request.query_params.get(
            "month"
        )

        year = request.query_params.get(
            "year"
        )

        if not employee_id:

            return Response(
                {
                    "error":
                    "employee parameter is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        today = timezone.localdate()

        month = int(month or today.month)
        year = int(year or today.year)

        records = Attendance.objects.filter(
            employee_id=employee_id,
            date__month=month,
            date__year=year
        )

        summary = {
            "present": records.filter(
                status="Present"
            ).count(),

            "absent": records.filter(
                status="Absent"
            ).count(),

            "half_day": records.filter(
                status="Half Day"
            ).count(),

            "late": records.filter(
                status="Late"
            ).count(),

            "permission": records.filter(
                status="Permission"
            ).count(),

            "leave": records.filter(
                status="Leave"
            ).count(),

            "overtime_hours": records.aggregate(
                total=Sum("overtime_hours")
            )["total"] or 0,
        }

        return Response(
            summary
        )


# ============================================================
# LEAVE VIEWSET
# ============================================================

class LeaveApplicationViewSet(
    viewsets.ModelViewSet
):

    queryset = LeaveApplication.objects.select_related(
        "employee",
        "approved_by"
    ).all()

    serializer_class = LeaveApplicationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = self.queryset

        employee = self.request.query_params.get(
            "employee"
        )

        leave_status = self.request.query_params.get(
            "status"
        )

        leave_type = self.request.query_params.get(
            "leave_type"
        )

        if employee:

            queryset = queryset.filter(
                employee_id=employee
            )

        if leave_status:

            queryset = queryset.filter(
                status=leave_status
            )

        if leave_type:

            queryset = queryset.filter(
                leave_type=leave_type
            )

        return queryset.order_by(
            "-id"
        )

    # --------------------------------------------------------
    # APPROVE
    # --------------------------------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="approve"
    )
    def approve(self, request, pk=None):

        leave = self.get_object()

        if leave.status == "Approved":

            return Response(
                {
                    "message":
                    "Leave is already approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        leave.status = "Approved"

        leave.approved_by = request.user

        leave.save(
            update_fields=[
                "status",
                "approved_by",
                "updated_at",
            ]
        )

        serializer = self.get_serializer(
            leave
        )

        return Response(
            serializer.data
        )

    # --------------------------------------------------------
    # REJECT
    # --------------------------------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="reject"
    )
    def reject(self, request, pk=None):

        leave = self.get_object()

        leave.status = "Rejected"

        leave.approved_by = request.user

        leave.admin_remarks = request.data.get(
            "admin_remarks",
            leave.admin_remarks
        )

        leave.save()

        serializer = self.get_serializer(
            leave
        )

        return Response(
            serializer.data
        )


# ============================================================
# BONUS VIEWSET
# ============================================================

class EmployeeBonusViewSet(
    viewsets.ModelViewSet
):

    queryset = EmployeeBonus.objects.select_related(
        "employee",
        "created_by"
    ).all()

    serializer_class = EmployeeBonusSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = self.queryset

        employee = self.request.query_params.get(
            "employee"
        )

        bonus_type = self.request.query_params.get(
            "bonus_type"
        )

        if employee:

            queryset = queryset.filter(
                employee_id=employee
            )

        if bonus_type:

            queryset = queryset.filter(
                bonus_type=bonus_type
            )

        return queryset.order_by(
            "-bonus_date",
            "-id"
        )

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )


# ============================================================
# GATE PASS VIEWSET
# ============================================================

class GatePassViewSet(
    viewsets.ModelViewSet
):

    queryset = GatePass.objects.select_related(
        "employee",
        "approved_by"
    ).all()

    serializer_class = GatePassSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = self.queryset

        employee = self.request.query_params.get(
            "employee"
        )

        pass_status = self.request.query_params.get(
            "status"
        )

        date = self.request.query_params.get(
            "date"
        )

        if employee:

            queryset = queryset.filter(
                employee_id=employee
            )

        if pass_status:

            queryset = queryset.filter(
                status=pass_status
            )

        if date:

            queryset = queryset.filter(
                date=date
            )

        return queryset.order_by(
            "-date",
            "-id"
        )

    # --------------------------------------------------------
    # APPROVE GATE PASS
    # --------------------------------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="approve"
    )
    def approve(self, request, pk=None):

        gate_pass = self.get_object()

        gate_pass.status = "Approved"

        gate_pass.approved_by = request.user

        gate_pass.save()

        serializer = self.get_serializer(
            gate_pass
        )

        return Response(
            serializer.data
        )

    # --------------------------------------------------------
    # REJECT GATE PASS
    # --------------------------------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="reject"
    )
    def reject(self, request, pk=None):

        gate_pass = self.get_object()

        gate_pass.status = "Rejected"

        gate_pass.approved_by = request.user

        gate_pass.remarks = request.data.get(
            "remarks",
            gate_pass.remarks
        )

        gate_pass.save()

        serializer = self.get_serializer(
            gate_pass
        )

        return Response(
            serializer.data
        )