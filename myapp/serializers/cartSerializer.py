from rest_framework import serializers
from myapp.Models import Cart, CartItem
from myapp.Models import Product
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), source='cart', write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product_id', 'product_name', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, required=False)  # Allow cart_items to be provided

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'cart_items']

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cart_items', [])
        cart = Cart.objects.create(**validated_data)
        for cart_item_data in cart_items_data:
            CartItem.objects.create(cart=cart, **cart_item_data)
        return cart

    def update(self, instance, validated_data):
        cart_items_data = validated_data.pop('cart_items', [])

        # Update cart instance
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        # Update or create CartItems
        existing_items = {item.product.id: item for item in instance.cart_items.all()}
        new_items = {item_data['product_id']: item_data for item_data in cart_items_data}

        # Delete items no longer in the cart
        for product_id, item in existing_items.items():
            if product_id not in new_items:
                item.delete()

        # Update existing items and create new items
        for product_id, item_data in new_items.items():
            if product_id in existing_items:
                item = existing_items[product_id]
                item.quantity = item_data['quantity']
                item.save()
            else:
                CartItem.objects.create(cart=instance, **item_data)

        return instance