from django.forms import ModelForm
from django import forms

from teacher.models import Teacher, Subject


class SubjectForm(ModelForm):
    class Meta:
        model = Subject

        fields = ['name', 'price', 'n_sessions']


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        widgets = {
            'date_joined': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'birthday': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['subject', 'name', 'address', 'certificate', 'major', 'phone', 'email',  'birthday', 'date_joined', 'salary']
