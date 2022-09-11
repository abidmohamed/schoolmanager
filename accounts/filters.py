import django_filters
from django.contrib.auth.models import User
from django_filters import *
from .models import *


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User

        fields = ['first_name', 'last_name', ]
