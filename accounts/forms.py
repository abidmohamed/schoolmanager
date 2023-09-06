from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json

# Form Layout from Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'floatingInput', 'class': 'form-control mb-3'}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'floatingPassword', 'class': 'form-control mb-3'}),
        required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
