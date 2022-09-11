from django.forms import ModelForm
from django import forms
from .models import *


class StudentPaymentFrom(ModelForm):
    class Meta:
        model = StudentPayment
        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['student', 'amount', 'pay_date', 'note']


class ParentPaymentForm(ModelForm):
    class Meta:
        model = ParentPayment
        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['parent', 'amount', 'pay_date', 'note']
