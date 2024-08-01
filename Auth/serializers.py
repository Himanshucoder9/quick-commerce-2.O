from rest_framework import serializers
from .models import User, Customer, Driver
from Master.myvalidator import mobile_validator


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "phone", "password"]


class PasswordResetSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=13,
        validators=[mobile_validator],
        help_text="Alphabets and special characters are not allowed.",
    )
    token = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'name', 'email', 'phone', 'gender', 'profile', 'dob', 'role', 'is_active', 'is_verified',]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "gender",
            "profile",
            "dob",
            "password",
            "role",
            "is_active",
            "is_verified",
        ]
        extra_kwargs = {
            "role": {
                "required": False
            },  # Role will be set in the VendorRegisterSerializer
            "is_active": {"required": False},
            "is_verified": {"required": False},
        }

    def get_profile(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.profile.url)
        return obj.profile.url


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


# class DriverSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Driver
#         fields = "__all__"
