# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Overriding the default to check for email instead of username
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user using email and password
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid email or password')

        attrs['username'] = user.username  # Token requires a username
        return super().validate(attrs)
