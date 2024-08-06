from rest_framework import serializers
from Auth.serializers import CustomerProfileSerializer
from Customer.models import ShippingAddress, Favorite, CartItem, Cart, OrderItem, Order, Payment
from Warehouse.serializers import SimpleProductSerializer, ProductSerializer


# ShippingAddress Serializers
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = (
            "id", "customer", "customer_name", "customer_phone", "address_type", "building_name", "floor", "landmark",
            "latitude", "longitude", "full_address", "created_at", "updated_at")


class DetailShippingAddressSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = (
            "id", "customer", "customer_name", "customer_phone", "address_type", "building_name", "floor", "landmark",
            "latitude", "longitude", "full_address", "created_at", "updated_at")


class FullShippingAddressSerializer(ShippingAddressSerializer):
    class Meta(ShippingAddressSerializer.Meta):
        fields = "__all__"


# Favorite Serializers
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            "id", "customer", "product", "created_at", "updated_at")


class DetailFavoriteSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(read_only=True)
    product = SimpleProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = (
            "id", "customer", "product", "created_at", "updated_at")


class FullFavoriteSerializer(FavoriteSerializer):
    class Meta(FavoriteSerializer.Meta):
        fields = "__all__"


# Cart Serializers

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    item_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "item_price"]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "customer", "cart_items"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "item_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "order_number", "shipping_address", "payment_method", "total_amount", "order_status",
                  "created_at", "items", ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)  # Save the Order instance first

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class DetailOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    shipping_address = DetailShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_number", "shipping_address", "payment_method", "total_amount", "order_status",
                  "created_at", "items", ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "order", "razorpay_order_id", "razorpay_payment_id", "razorpay_payment_status", "amount",
                  "payment_status",
                  "payment_method"]
        read_only_fields = ["razorpay_order_id", ]
