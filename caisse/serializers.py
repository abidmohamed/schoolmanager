from rest_framework import serializers
from .models import TransactionCategory, Transaction

class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = '__all__'  # You can specify the fields you want to include if needed

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # You can specify the fields you want to include if needed
