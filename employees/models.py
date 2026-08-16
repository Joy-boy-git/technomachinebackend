from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# ============================================================
# EMPLOYEE
# ============================================================

class Employee(models.Model):

    EMPLOYMENT_TYPE_CHOICES = [
        ("Permanent", "Permanent"),
        ("Temporary", "Temporary"),
        ("Contract", "Contract"),
        ("Intern", "Intern"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Resigned", "Resigned"),
        ("Terminated", "Terminated"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile"
    )

    # --------------------------------------------------------
    # PERSONAL DETAILS
    # --------------------------------------------------------

    full_name = models.CharField(
        max_length=255
    )

    photo = models.ImageField(
        upload_to="employees/photos/",
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        default=""
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    email = models.EmailField(
        blank=True,
        default=""
    )

    address = models.TextField(
        blank=True,
        default=""
    )

    emergency_contact_name = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    emergency_contact_phone = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    # --------------------------------------------------------
    # JOB DETAILS
    # --------------------------------------------------------

    department = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    joining_date = models.DateField(
        default=timezone.localdate
    )

    employment_type = models.CharField(
        max_length=30,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="Permanent"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Active"
    )

    # --------------------------------------------------------
    # SALARY
    # --------------------------------------------------------

    basic_salary = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    allowances = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    overtime_rate = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # --------------------------------------------------------
    # LEAVE
    # --------------------------------------------------------

    annual_leave_balance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00")
    )

    sick_leave_balance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # --------------------------------------------------------
    # BANK DETAILS
    # --------------------------------------------------------

    bank_name = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    account_number = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    ifsc_code = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"


# ============================================================
# ATTENDANCE
# ============================================================

class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Half Day", "Half Day"),
        ("Late", "Late"),
        ("Permission", "Permission"),
        ("Leave", "Leave"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    date = models.DateField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES
    )

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    overtime_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00")
    )

    remarks = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "date"],
                name="unique_employee_attendance"
            )
        ]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date}"


# ============================================================
# LEAVE APPLICATION
# ============================================================

class LeaveApplication(models.Model):

    LEAVE_TYPE_CHOICES = [
        ("Casual Leave", "Casual Leave"),
        ("Sick Leave", "Sick Leave"),
        ("Annual Leave", "Annual Leave"),
        ("Emergency Leave", "Emergency Leave"),
        ("Unpaid Leave", "Unpaid Leave"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_applications"
    )

    leave_type = models.CharField(
        max_length=50,
        choices=LEAVE_TYPE_CHOICES
    )

    from_date = models.DateField()

    to_date = models.DateField()

    number_of_days = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00")
    )

    reason = models.TextField(
        blank=True,
        default=""
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    admin_remarks = models.TextField(
        blank=True,
        default=""
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_employee_leaves"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.leave_type}"
        )


# ============================================================
# BONUS
# ============================================================

class EmployeeBonus(models.Model):

    BONUS_TYPE_CHOICES = [
        ("Special Bonus", "Special Bonus"),
        ("Festival Bonus", "Festival Bonus"),
        ("Performance Bonus", "Performance Bonus"),
        ("Other", "Other"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="bonuses"
    )

    bonus_type = models.CharField(
        max_length=50,
        choices=BONUS_TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    bonus_date = models.DateField(
        default=timezone.localdate
    )

    reason = models.TextField(
        blank=True,
        default=""
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-bonus_date", "-id"]

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.bonus_type}"
        )


# ============================================================
# GATE PASS
# ============================================================

class GatePass(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
    ]

    PASS_TYPE_CHOICES = [
        ("Personal", "Personal"),
        ("Official", "Official"),
        ("Emergency", "Emergency"),
        ("Other", "Other"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="gate_passes"
    )

    date = models.DateField(
        default=timezone.localdate
    )

    pass_type = models.CharField(
        max_length=30,
        choices=PASS_TYPE_CHOICES,
        default="Personal"
    )

    out_time = models.TimeField(
        null=True,
        blank=True
    )

    in_time = models.TimeField(
        null=True,
        blank=True
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_gate_passes"
    )

    remarks = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.date}"
        )