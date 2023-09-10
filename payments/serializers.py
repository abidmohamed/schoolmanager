from rest_framework import serializers
from .models import StudentPayment, ParentPayment, Payroll


class StudentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPayment
        fields = '__all__'


class ParentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentPayment
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'
