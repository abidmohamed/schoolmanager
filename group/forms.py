from django.forms import ModelForm
from django import forms

from group.models import Room, Group, GroupTime


class RoomForm(ModelForm):
    class Meta:
        model = Room

        fields = ['name']


class GroupForm(ModelForm):
    class Meta:
        model = Group

        fields = ['subject', 'teacher', 'name', 'group_type']


class GroupTimeForm(ModelForm):
    class Meta:
        model = GroupTime
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'timepicker', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'timepicker', 'type': 'time'}),
        }
        fields = ['group', 'weekday', 'start_time', 'end_time', 'room', 'hallway']
