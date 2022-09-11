import django_filters
from django_filters import CharFilter, DateFilter
from .models import *


class TransactionFilter(django_filters.FilterSet):
    name = CharFilter(field_name='Transaction_name', lookup_expr='icontains')
    start_date = DateFilter(field_name='trans_date', lookup_expr="gte")
    end_date = DateFilter(field_name='trans_date', lookup_expr="lte")

    class Meta:
        model = Transaction

        fields = ['name', 'category', 'Transaction_type', 'start_date', 'end_date']


class TransactionCategoryFilter(django_filters.FilterSet):

    class Meta:
        model = TransactionCategory

        fields = ['name']