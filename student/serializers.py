from rest_framework import serializers
from .models import Parent, Kids, Student


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class KidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kids
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
