from rest_framework import serializers
from Auth.models import User, Customer, Driver, WareHouse
from Master.myvalidator import mobile_validator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("name", "email", "phone", "password")


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone", "gender", "profile", "dob", "is_active", "role")


class WareHouseRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = (
            "role",
            "name",
            "email",
            "phone",
            "dob",
            "gender",
            "profile",
            "warehouse_name",
            "license",
            "identity",
            "document",
            "gst_no",
            "fssai_no",
            "operation_area",
            "warehouse_image",
            "warehouse_image_owner",
            "password",
        )


class WareHouseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = (
            "id", "warehouse_id", "warehouse_name", "name", "email", "phone", "gender", "profile", "dob", "is_active",
            "role")


class DriverRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("name", "email", "phone", "password")


class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("id", "name", "email", "phone", "gender", "profile", "dob", "is_active", "role")
