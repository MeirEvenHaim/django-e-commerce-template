from django.contrib.auth import get_user_model
# myapp/serializers/userSerializer.py
from rest_framework import serializers
from django.contrib.auth.models import User
from myapp.Models import Client

# myapp/serializers/userSerializer.py


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Assuming you want to create a Client instance with the user
        Client.objects.create(user=user)  # Create associated Client instance
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Add any other fields you want to display