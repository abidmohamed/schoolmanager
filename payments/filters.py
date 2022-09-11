import django_filters
from django import forms
from django_filters import CharFilter, DateFilter, DateRangeFilter
from .models import *


class StudentPaymentFilter(django_filters.FilterSet):
    student = CharFilter(field_name='student__name', lookup_expr='icontains')
    start_date = DateFilter(field_name='pay_date', lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='pay_date', lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        fields = ['student', 'start_date', 'end_date', ]


class ParentPaymentFilter(django_filters.FilterSet):
    parent = CharFilter(field_name='parent__name', lookup_expr='icontains')
    start_date = DateFilter(field_name='pay_date', lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='pay_date', lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        fields = ['parent', 'start_date', 'end_date', ]


class PayrollFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='pay_date', lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='pay_date', lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:

        fields = ['pay_type', 'start_date', 'end_date']
