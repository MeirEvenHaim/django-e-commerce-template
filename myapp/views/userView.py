from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from myapp.serializers.userSerializer import UserCreateSerializer, UserSerializer
from myapp.Models import Client
from myapp.permissions import IsAdminOrSelf

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Require authentication for all actions

    def get_permissions(self):
        if self.action in ['list', 'destroy', 'update', 'partial_update']:
            # Only admin can list all users or delete/update others
            self.permission_classes = [IsAdminOrSelf]
        elif self.action == 'retrieve':
            # Regular users can retrieve only their own information
            self.permission_classes = [IsAdminOrSelf]
        return super().get_permissions()

    # Admin can view all users
    def list(self, request):
        users = Client.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # Admin or regular user can view their own profile
    def retrieve(self, request, pk=None):
        try:
            user = Client.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Admin or the user himself can update their profile
    def update(self, request, pk=None):
        try:
            user = Client.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            serializer = UserCreateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Admin can delete any user
    def destroy(self, request, pk=None):
        try:
            user = Client.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Client.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)