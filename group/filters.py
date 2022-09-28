import django_filters
from django import forms
from django_filters import CharFilter, DateFilter, DateRangeFilter
from .models import *


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group

        fields = ['teacher', 'room', 'subject', 'name', 'group_type']


class GroupTimeFilter(django_filters.FilterSet):
    class Meta:
        model = GroupTime
        start_time = DateFilter(field_name='start_time', lookup_expr="gte",
                                widget=forms.DateInput(attrs={'type': 'time'}))
        end_time = DateFilter(field_name='end_time', lookup_expr="lte",
                              widget=forms.DateInput(attrs={'type': 'time'}))

        fields = ['group', 'start_time', 'end_time', 'weekday', 'room']
