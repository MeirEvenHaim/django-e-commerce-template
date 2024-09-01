from django.shortcuts import get_object_or_404
from rest_framework import serializers
from myapp.Models import Cart, CartItem, Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

    def validate(self, data):
        cart = data.get('cart')
        # Ensure the cart belongs to the client making the request
        if not self.context['request'].user.is_staff and cart.client != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to add items to this cart.")
        return data

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)
    
    
class CartItemsSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    items = CartItemSerializer(many=True)

    def validate_cart_id(self, value):
        if not Cart.objects.filter(id=value).exists():
            raise serializers.ValidationError("The specified cart does not exist.")
        return value

    def validate(self, data):
        cart_id = data.get('cart_id')
        items_data = data.get('items')

        # Debugging: Check if product IDs are being passed correctly
        product_ids = [item['product'] for item in items_data]
        print(f"Received Product IDs: {product_ids}")  # Debugging log

        # Validate each product
        if not all(Product.objects.filter(id=product_id).exists() for product_id in product_ids):
            raise serializers.ValidationError("One or more products do not exist.")
        
        return data

    def create(self, validated_data):
        cart_id = validated_data.get('cart_id')
        items_data = validated_data.get('items')
        cart = Cart.objects.get(id=cart_id)

        cart_items = []
        for item_data in items_data:
            item_data['cart'] = cart
            cart_item = CartItemSerializer().create(item_data)
            cart_items.append(cart_item)

        return cart_items
    
    
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, required=False)  # Allow cart_items to be provided

    class Meta:
        model = Cart
        fields = ['id', 'client', 'created_at', 'cart_items']  # Changed 'user' to 'client'

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cart_items', [])
        cart = Cart.objects.create(**validated_data)
        for cart_item_data in cart_items_data:
            CartItem.objects.create(cart=cart, **cart_item_data)
        return cart

    def update(self, instance, validated_data):
        cart_items_data = validated_data.pop('cart_items', [])

        # Update cart instance
        instance.client = validated_data.get('client', instance.client)  # Changed 'user' to 'client'
        instance.save()

        # Update or create CartItems
        existing_items = {item.product.id: item for item in instance.cart_items.all()}
        new_items = {item_data['product']: item_data for item_data in cart_items_data}

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