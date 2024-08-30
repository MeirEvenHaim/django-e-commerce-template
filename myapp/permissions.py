from rest_framework.permissions import BasePermission

from myapp.Models import Cart, CartItem
class IsAdminOrSelf(BasePermission):
    """
    Custom permission to allow only admin to perform any action
    and regular users to retrieve or update their own profile.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can perform any action
        if request.user.role == 'admin':
            return True
        # Regular users can only view/update their own profile
        return obj == request.user
    


class IsAdminOrOwner(BasePermission):
    """
    Custom permission to only allow admins to access all objects,
    while regular users can only access their own carts and cart items.
    """
    def has_object_permission(self, request, view, obj):
        # Admins have access to everything
        if request.user.is_staff:
            return True
        
        # Regular users can only access their own carts and cart items
        if isinstance(obj, Cart):
            return obj.user == request.user
        
        if isinstance(obj, CartItem):
            return obj.cart.user == request.user
        
        return False

    def has_permission(self, request, view):
        # Admins can access any view
        if request.user.is_staff:
            return True
        
        # Regular users should be authenticated to access their carts
        if request.method in ['GET']:
            return request.user.is_authenticated
        
        return False
