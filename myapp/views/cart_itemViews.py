from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.Models import Cart, CartItem, Product
from myapp.serializers.cartSerializer import CartItemSerializer, CartItemsSerializer
from myapp.permissions import IsAdminOrOwner
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminOrOwner])
def cart_item_list(request):
    if request.method == 'GET':
        if request.user.is_staff:
            cart_items = CartItem.objects.all()
        else:
            cart_items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        cart_id = request.data.get('cart_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        # Validate cart_id and product_id
        if not Cart.objects.filter(pk=cart_id).exists():
            return Response({'cart_id': 'Invalid cart ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if not Product.objects.filter(pk=product_id).exists():
            return Response({'product_id': 'Invalid product ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the CartItem
        cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrOwner])
def cart_item_detail(request, pk):
    try:
        cart_item = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
