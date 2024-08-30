from rest_framework import serializers
from myapp.Models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    cart_id = serializers.ReadOnlyField(source='cart.id')

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'cart_id', 'product', 'product_name', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'cart_items']
