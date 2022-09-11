import django_filters
from django import forms
from django_filters import CharFilter, DateFilter, DateRangeFilter
from .models import *


class EmployeeAttendanceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='attendance_date', lookup_expr="gte",
                            widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='attendance_date', lookup_expr="lte",
                          widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = EmployeeAttendance

        fields = ['start_date', 'end_date']


class EmployeeAttendanceItemFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='attendance__attendance_date', lookup_expr="gte",
                            widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='attendance__attendance_date', lookup_expr="lte",
                          widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = EmployeeAttendanceItem

        fields = ['start_date', 'end_date']


class TeacherAttendanceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='attendance__attendance_date', lookup_expr="gte",
                            widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='attendance__attendance_date', lookup_expr="lte",
                          widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TeacherAttendanceItem

        fields = ['start_date', 'end_date']


class StudentAttendanceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='attendance__attendance_date', lookup_expr="gte",
                            widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='attendance__attendance_date', lookup_expr="lte",
                          widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = StudentAttendanceItem

        fields = ['start_date', 'end_date']