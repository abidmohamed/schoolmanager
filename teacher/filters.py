import django_filters
from django import forms
from django_filters import CharFilter, DateFilter, DateRangeFilter
from .models import *


class SubjectFilter(django_filters.FilterSet):

    class Meta:
        model = Subject

        fields = ['name', 'price']


class TeacherFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_joined', lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='date_joined', lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Teacher

        fields = ['name', 'certificate', 'major', 'phone', 'start_date', 'end_date']
