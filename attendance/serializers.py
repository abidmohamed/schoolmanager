from rest_framework import serializers
from .models import StudentAttendance, StudentAttendanceItem, EmployeeAttendance, EmployeeAttendanceItem, \
    EmployeeLeaveItem, TeacherAttendanceItem, TeacherLeaveItem, SessionCounter, TeacherSessionCounter


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'


class StudentAttendanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendanceItem
        fields = '__all__'


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = '__all__'


class EmployeeAttendanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendanceItem
        fields = '__all__'


class EmployeeLeaveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveItem
        fields = '__all__'


class TeacherAttendanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendanceItem
        fields = '__all__'


class TeacherLeaveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherLeaveItem
        fields = '__all__'


class SessionCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionCounter
        fields = '__all__'


class TeacherSessionCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSessionCounter
        fields = '__all__'
