from rest_framework import serializers
from myapp.Models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_price', 'status', 'created_at']
