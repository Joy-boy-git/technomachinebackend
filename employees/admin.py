from django.contrib import admin

from .models import (
    Employee,
    Attendance,
    LeaveApplication,
    EmployeeBonus,
    GatePass,
)


# ============================================================
# EMPLOYEE ADMIN
# ============================================================

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "full_name",
        "department",
        "designation",
        "employment_type",
        "basic_salary",
        "status",
        "joining_date",
    )

    list_filter = (
        "department",
        "employment_type",
        "status",
        "joining_date",
    )

    search_fields = (
        "employee_id",
        "full_name",
        "phone",
        "email",
        "department",
        "designation",
    )

    ordering = (
        "-id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ============================================================
# ATTENDANCE ADMIN
# ============================================================

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "date",
        "status",
        "check_in",
        "check_out",
        "overtime_hours",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "employee__employee_id",
        "employee__full_name",
    )

    ordering = (
        "-date",
    )


# ============================================================
# LEAVE APPLICATION ADMIN
# ============================================================

@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "leave_type",
        "from_date",
        "to_date",
        "number_of_days",
        "status",
        "approved_by",
        "created_at",
    )

    list_filter = (
        "leave_type",
        "status",
        "from_date",
    )

    search_fields = (
        "employee__employee_id",
        "employee__full_name",
        "reason",
    )

    ordering = (
        "-id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ============================================================
# BONUS ADMIN
# ============================================================

@admin.register(EmployeeBonus)
class EmployeeBonusAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "bonus_type",
        "amount",
        "bonus_date",
        "created_by",
    )

    list_filter = (
        "bonus_type",
        "bonus_date",
    )

    search_fields = (
        "employee__employee_id",
        "employee__full_name",
        "reason",
    )

    ordering = (
        "-bonus_date",
        "-id",
    )

    readonly_fields = (
        "created_at",
    )


# ============================================================
# GATE PASS ADMIN
# ============================================================

@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "date",
        "pass_type",
        "out_time",
        "in_time",
        "status",
        "approved_by",
    )

    list_filter = (
        "pass_type",
        "status",
        "date",
    )

    search_fields = (
        "employee__employee_id",
        "employee__full_name",
        "reason",
    )

    ordering = (
        "-date",
        "-id",
    )

    readonly_fields = (
        "created_at",
    )