import django_filters
from django import forms
from django_filters import CharFilter, DateFilter, DateRangeFilter
from .models import *


class ParentFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    start_date = DateFilter(field_name='date_joined', lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='date_joined', lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Parent

        fields = ['name', 'province', 'phone', 'start_date', 'end_date']


class KidsFilter(django_filters.FilterSet):
    parent = CharFilter(field_name='parent__name', lookup_expr='icontains')

    class Meta:
        model = Kids

        fields = ['parent', 'name', 'grade', 'sick']


class StudentFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    date_range = DateRangeFilter(field_name='date_joined')

    class Meta:
        model = Student

        fields = ['name', 'province', 'phone', 'date_range']
