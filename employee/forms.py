from django.forms import ModelForm
from django import forms
from employee.models import Employee, Role


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee

        widgets = {
            'date_joined': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'birth_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['name', 'address', 'province', 'gender', 'martial_status', 'phone', 'email', 'birth_date',
                  'role', 'date_joined', 'is_active']


class RoleForm(ModelForm):
    class Meta:
        model = Role

        fields = ['name', 'salary', ]
