from rest_framework import serializers
from myapp.Models import Payment, Order

class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())  # Reference the order

    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_date', 'amount', 'payment_method', 'transaction_id', 'status']

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment
