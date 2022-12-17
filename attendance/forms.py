from django.forms import ModelForm
from django import forms

from attendance.models import StudentAttendance, EmployeeAttendance


class StudentAttendanceForm(ModelForm):
    class Meta:
        model = StudentAttendance

        widgets = {
            'attendance_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'attendance_time': forms.DateInput(attrs={'class': 'timepicker', 'type': 'time'}),
        }
        fields = ['attendance_date', 'attendance_time']


class EmployeeAttendanceForm(ModelForm):
    class Meta:
        model = EmployeeAttendance

        widgets = {
            'attendance_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['attendance_date', ]

