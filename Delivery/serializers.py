from rest_framework import serializers
from Auth.serializers import CustomerProfileSerializer, DriverProfileSerializer
from Customer.serializers import DetailOrderSerializer
from Delivery.models import Delivery


# Delivery Serializers
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            "id", "status", "driver", "delivery_radius", "orders", "otp", "otp_created_at", "created_at", "updated_at")


class DetailDeliverySerializer(serializers.ModelSerializer):
    driver = DriverProfileSerializer(read_only=True)
    orders = DetailOrderSerializer(read_only=True, many=True)

    class Meta:
        model = Delivery
        fields = (
            "id", "status", "driver", "delivery_radius", "orders", "created_at", "updated_at")


class FullDeliverySerializer(DeliverySerializer):
    class Meta(DeliverySerializer.Meta):
        fields = "__all__"
