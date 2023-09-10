from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'  # Include all fields from the Event model


# Optionally, if you want to customize the serialization of specific fields:
class CustomEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('day', 'start_time', 'end_time', 'event_type', 'notes')  # Specify the fields you want to include

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # You can customize the representation of fields here if needed
        # For example, format dates or times differently
        data['day'] = instance.day.strftime('%Y-%m-%d')
        data['start_time'] = instance.start_time.strftime('%H:%M:%S')
        data['end_time'] = instance.end_time.strftime('%H:%M:%S')
        return data

#
# In the code above:
#
# EventSerializer is a serializer for the Event model that includes all fields. CustomEventSerializer is a custom
# serializer that includes only specific fields (day, start_time, end_time, event_type, and notes). It also overrides
# the to_representation method to customize the representation of fields (e.g., formatting dates and times).
#
# You can choose to use either the EventSerializer or CustomEventSerializer in your Django REST framework views based on your serialization needs.
