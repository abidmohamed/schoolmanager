from django.db.models import Q

from attendance.models import EmployeeAttendanceItem, TeacherAttendanceItem
from employee.models import Employee
from payments.models import Payroll
from teacher.models import Teacher
from datetime import datetime


def update_payment():
    employees = Employee.objects.all().filter(is_active=True)
    teachers = Teacher.objects.all().filter(is_active=True)
    # employees
    for employee in employees:
        # calculate salary
        # 1 get attendance
        attendance_present = EmployeeAttendanceItem.objects.filter(Q(status='PRESENT') | Q(status='MISSION'),
                                                                   employee=employee,
                                                                   attendance__attendance_date__month=datetime.now().month,
                                                                   attendance__attendance_date__year=datetime.now().year
                                                                   ).count()
        # 2 get salary by day and calculate
        day_salary = employee.role.salary / 26
        salary = attendance_present * day_salary
        # 3 create payroll object
        Payroll.objects.create(
            employee=employee,
            amount=salary,
            pay_date=datetime.now().date(),
            pay_type="EMPLOYEE",
        )
    # teachers
    for teacher in teachers:
        # calculate salary
        # 1 get attendance
        attendance_present = TeacherAttendanceItem.objects.filter(teacher=teacher, status='PRESENT',
                                                                  attendance__attendance_date__month=datetime.now().month).count()
        # 2 get salary by day and calculate
        day_salary = teacher.salary / 26
        salary = attendance_present * day_salary
        # 3 create payroll object
        Payroll.objects.create(
            teacher=teacher,
            amount=salary,
            pay_date=datetime.now().date(),
            pay_type="TEACHER",
        )
