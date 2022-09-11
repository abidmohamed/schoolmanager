from django.forms import ModelForm
from django import forms

from student.models import Parent, Kids, Student


class ParentForm(ModelForm):
    class Meta:
        model = Parent
        widgets = {
            'date_joined': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['name', 'address', 'province', 'phone', 'email', 'date_joined',]


class KidsForm(ModelForm):
    class Meta:
        model = Kids
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['name', 'grade', 'sick', 'description', 'birthday', 'is_active', 'transportation']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        widgets = {
            'date_joined': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'birthday': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['name', 'address', 'province', 'phone', 'email', 'birthday', 'date_joined', 'is_active', 'transportation']
