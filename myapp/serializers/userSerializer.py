
from rest_framework import serializers
from django.contrib.auth.models import User
from myapp.Models import Client

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField(required=False, default=False)  # Optional field
    is_superuser = serializers.BooleanField(required=False, default=False)  # Optional field

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

# Serializer for the Client model
class ClientSerializer(serializers.ModelSerializer):
    # Include fields from the Client model as necessary
    # If Client should have a related User model, adjust accordingly
    user = UserCreateSerializer()
    class Meta:
        model = Client
        fields = ['id', 'additional_info']  # Adjust fields as necessary

# JWT Token Serializer
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()