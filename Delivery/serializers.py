from rest_framework import serializers
from Auth.serializers import DriverProfileSerializer
from Customer.serializers import DetailOrderSerializer
from Delivery.models import DeliveryAddress
from Auth.models import Driver


# Delivery Serializers
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = (
            "id", "status", "driver", "delivery_radius", "orders", "otp", "otp_created_at", "created_at", "updated_at")


class DetailDeliverySerializer(serializers.ModelSerializer):
    driver = DriverProfileSerializer(read_only=True)
    orders = DetailOrderSerializer(read_only=True, many=True)

    class Meta:
        model = DeliveryAddress
        fields = (
            "id", "status", "driver", "delivery_radius", "orders", "created_at", "updated_at")


class FullDeliverySerializer(DeliverySerializer):
    class Meta(DeliverySerializer.Meta):
        fields = "__all__"


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ["id", "status", "otp", "otp_created_at"]


class CustomerDeliveryStatusSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="orders.first.order_number")
    delivery_status = serializers.CharField(source="status")
    driver_name = serializers.CharField(source="driver.name", default="Not assigned")
    driver_phone = serializers.CharField(source="driver.phone", default="Not assigned")

    class Meta:
        model = DeliveryAddress
        fields = ["order_number", "delivery_status", "driver_name", "driver_phone"]