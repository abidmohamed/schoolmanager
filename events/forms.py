from django import forms

from events.models import Event


class EventFrom(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'timepicker', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'timepicker', 'type': 'time'}),
            'day': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['day', 'start_time', 'end_time', 'event_type', 'notes']