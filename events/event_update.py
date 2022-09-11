from datetime import datetime

from employee.models import Employee
from events.models import Event
from student.models import Kids, Student
from teacher.models import Teacher


def update_event():
    # birthday
    teachers = Teacher.objects.filter(is_active=True)
    employees = Employee.objects.filter(is_active=True)
    kids = Kids.objects.filter(is_active=True)
    students = Student.objects.filter(is_active=True)

    for employee in employees:
        if employee.birth_date.month == datetime.now().month:
            Event.objects.create(
                day=employee.birth_date,
                start_time=8,
                end_time=10,
                notes='{} {}'.format(employee.name, "BIRTHDAY"),
                event_type="MANAGEMENT",
            )

    for teacher in teachers:
        if teacher.birthday.month == datetime.now().month:
            Event.objects.create(
                day=teacher.birthday,
                start_time=8,
                end_time=10,
                notes='{} {}'.format(teacher.name, "BIRTHDAY"),
                event_type="TEACHERS",
            )

    for kid in kids:
        if kid.birthday.month == datetime.now().month:
            Event.objects.create(
                day=teacher.birthday,
                start_time=8,
                end_time=10,
                notes='{} {}'.format(kid.name, "BIRTHDAY"),
                event_type="TEACHERS",
            )

    for student in students:
        if student.birthday.month == datetime.now().month:
            Event.objects.create(
                day=teacher.birthday,
                start_time=8,
                end_time=10,
                notes='{} {}'.format(student.name, "BIRTHDAY"),
                event_type="TEACHERS",
            )
