import django_filters
from django.contrib.auth.models import User
from django_filters import *
from .models import *


class UserFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name="first_name", lookup_expr='icontains')
    last_name = CharFilter(field_name="last_name", lookup_expr='icontains')

    class Meta:
        model = User

        fields = ['first_name', 'last_name', ]
