from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from myapp.serializers.userSerializer import UserCreateSerializer
from django.core.mail import send_mail
from django.conf import settings
from myapp.Models import Client

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the username from the validated data
            username = serializer.validated_data.get('username')
            
            # Check if the username already exists
            if Client.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save the user (and the associated Client instance)
            user = serializer.save()
            self.send_welcome_email(user.email)  # Send welcome email
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_welcome_email(self, email):
        subject = "Welcome to MyApp"
        message = "Thank you for registering with MyApp. We're glad to have you on board!"
        from_email = settings.DEFAULT_FROM_EMAIL  # Make sure this is configured in settings.py
        recipient_list = [email]
        
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,  # Will raise an exception if the email fails to send
        )
