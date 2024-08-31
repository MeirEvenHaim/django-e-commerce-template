from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.Models import Cart , Client
from myapp.serializers.cartSerializer import CartSerializer
from myapp.permissions import IsAdminOrOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminOrOwner])

def cart_list(request):
    if request.method == 'GET':
        if request.user.is_staff:
            carts = Cart.objects.all()
        else:
            carts = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure that we're assigning a Client instance
            client = get_object_or_404(Client, user=request.user)
            serializer.save(user=client)  # Assign Client to cart
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrOwner])
def cart_detail(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
