from rest_framework import serializers
from myapp.Models import Shipping

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'order', 'address', 'tracking_number', 'status']
