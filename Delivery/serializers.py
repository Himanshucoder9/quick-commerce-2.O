from rest_framework import serializers
from Auth.serializers import CustomerProfileSerializer
from Delivery.models import Delivery


# Delivery Serializers
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            "id", "status", "driver", "delivery_radius", "orders", "otp", "otp_created_at", "created_at", "updated_at")


class FullDeliverySerializer(DeliverySerializer):
    class Meta(DeliverySerializer.Meta):
        fields = "__all__"
