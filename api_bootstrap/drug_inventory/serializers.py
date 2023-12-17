from rest_framework import serializers
from .models import Drug, Category, Transaction

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
