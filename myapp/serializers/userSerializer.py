from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from myapp.Models import Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
# Serializer for creating a new user (client)
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Serializer for the Client model
class ClientSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Client
        fields = ['id', 'user', 'additional_info']

# JWT Token Serializer
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()  # Add email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Include email in fields

    def create(self, validated_data):
        # Extract the password and email from validated_data
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        # Create the user with email and password
        user = User(
            username=validated_data['username'],
            email=email
        )
        user.set_password(password)
        user.save()
        return user