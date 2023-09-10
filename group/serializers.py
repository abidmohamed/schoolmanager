from rest_framework import serializers
from .models import Room, Group, GroupStudent, GroupTime


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = '__all__'


class GroupTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTime
        fields = '__all__'
