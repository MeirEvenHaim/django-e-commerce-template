from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.Models import Cart, Client
from myapp.serializers.cartSerializer import CartSerializer
from myapp.permissions import IsAdminOrOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminOrOwner])
def cart_list(request):
    if request.method == 'GET':
        if request.user.is_staff:
            # Admins can view all carts
            carts = Cart.objects.all()
        else:
            # Clients can only view their own carts
            client = get_object_or_404(Client, user=request.user)
            carts = Cart.objects.filter(user=client)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # If the user is an admin, allow cart creation without client restrictions
        if request.user.is_staff:
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # Admin can create a cart for any client
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # For normal clients, ensure that they can only create carts for themselves
        else:
            client = get_object_or_404(Client, user=request.user)

            # Ensure that the user can only create a cart for their own client
            requested_client_id = request.data.get('client')

            # If the client ID is provided and it doesn't match the current user's client ID, raise an error
            if requested_client_id and int(requested_client_id) != client.id:
                raise ValidationError("You can only create a cart for yourself.")

            # Proceed to save the cart for the logged-in user's client
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=client)  # Associate the cart with the current client
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrOwner])
def cart_detail(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # If the user is an admin, they have full access to GET, PUT, DELETE any cart
    if request.user.is_staff:
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
    
    # For non-admin users (clients), they can only modify or delete their own cart
    else:
        client = get_object_or_404(Client, user=request.user)

        # Ensure that the cart belongs to the logged-in user's client
        if cart.user != client:
            raise ValidationError("You can only modify or delete your own cart.")
        
        # Handle GET, PUT, DELETE for non-admins
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