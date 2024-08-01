from rest_framework import serializers
from .models import User, Customer, Driver
from Master.myvalidator import mobile_validator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "phone", "password"]

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone','gender','profile','dob',]

class PasswordResetSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=13,
        validators=[mobile_validator],
        help_text="Alphabets and special characters are not allowed.",
    )
    token = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token