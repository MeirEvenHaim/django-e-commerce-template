from django.contrib.auth import get_user_model
# myapp/serializers/userSerializer.py
from rest_framework import serializers
from django.contrib.auth.models import User
from myapp.Models import Client

# myapp/serializers/userSerializer.py


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['email', 'username', 'password']
    
    def validate_username(self, value):
        if Client.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def create(self, validated_data):
        # Create and return a new `Client` instance, using the validated data.
        return Client.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Add any other fields you want to display