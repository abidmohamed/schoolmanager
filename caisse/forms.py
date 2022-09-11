from django.forms import ModelForm
from django import forms

from caisse.models import Transaction, TransactionCategory


class CategoryTransactionForm(ModelForm):
    class Meta:
        model = TransactionCategory

        fields = ['name']


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        widgets = {
            'trans_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'desc': forms.Textarea(),
        }
        fields = ['Transaction_name', 'category', 'amount', 'Transaction_type', 'trans_date', 'desc']


# Specify Limit Year
YEARS = [x for x in range(2000, 2200)]


class DateForm(forms.Form):
    date = forms.DateTimeField(initial="2021-01-01",
                               widget=forms.DateInput(attrs={
                                   'class': 'form-control', 'type': 'text'
                               })
                               )


class PeriodForm(forms.Form):
    start_date = forms.DateTimeField(initial="2021-01-01",
                                     widget=forms.DateInput(attrs={
                                         'class': 'form-control datepicker', 'type': 'date'
                                     })
                                     )
    end_date = forms.DateTimeField(initial="2021-01-01",
                                   widget=forms.DateInput(attrs={
                                       'class': 'form-control datepicker', 'type': 'date'
                                   })
                                   )
