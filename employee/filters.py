import django_filters
from django import forms
from django_filters import CharFilter, DateFilter, DateRangeFilter
from .models import *


class EmployeeFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    phone = CharFilter(field_name='phone', lookup_expr='icontains')

    start_date = DateFilter(field_name='date_joined', lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='date_joined', lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Employee

        fields = ['name', 'province', 'role', 'gender', 'phone', 'start_date', 'end_date']


class RoleFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Role

        fields = ['name',]
