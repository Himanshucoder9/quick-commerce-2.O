import logging
import razorpay
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, request
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from Customer.models import ShippingAddress, Favorite, Cart, CartItem, Order, OrderItem, Payment
from Customer.serializers import ShippingAddressSerializer, FullShippingAddressSerializer, FullFavoriteSerializer, \
    CartSerializer, CartItemSerializer, OrderSerializer, FavoriteSerializer, DetailFavoriteSerializer
from Warehouse.models import Product
from rest_framework.exceptions import NotFound

logger = logging.getLogger(__name__)


# Shipping Address Views
class ShippingAddressListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        queryset = ShippingAddress.objects.filter(customer=customer)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        message = "Shipping addresses retrieved successfully" if queryset.exists() else "No shipping address available"
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class ShippingAddressRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = FullShippingAddressSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']

    def get_queryset(self):
        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        queryset = ShippingAddress.objects.filter(customer=customer)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Address updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Favorite Views
class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        queryset = Favorite.objects.filter(customer=customer)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No data available."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DetailFavoriteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        if Favorite.objects.filter(customer=request.user.customer, product_id=product_id).exists():
            return Response({"message": "Product is already in favorites"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user.customer)
        return Response({"message": "Product added to favorites", "data": serializer.data},
                        status=status.HTTP_201_CREATED)


# Cart Views
class CartAddProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        cart_items_data = request.data.get("cart_items")

        if not cart_items_data:
            return Response({"error": "No cart items provided"}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(customer=customer)

        for item_data in cart_items_data:
            product_id = item_data.get("product_id")
            quantity = item_data.get("quantity", 1)

            if not product_id:
                return Response({"error": "Product ID not provided for an item"}, status=status.HTTP_400_BAD_REQUEST)

            product = get_object_or_404(Product, pk=product_id)

            if quantity <= 0:
                return Response({"error": f"Please enter a quantity greater than 0 for product ID {product_id}"},
                                status=status.HTTP_400_BAD_REQUEST)

            if product.stock_quantity < quantity:
                return Response({"error": f"Not enough stock available for product ID {product_id}",
                                 "available_quantity": product.stock_quantity}, status=status.HTTP_400_BAD_REQUEST)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()

        return Response({"message": "Products successfully added to cart"}, status=status.HTTP_201_CREATED)


class CartRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"message": "No items in your cart."}, status=status.HTTP_200_OK)

        total_quantity = sum(cart_item.quantity for cart_item in cart_items)
        serializer = CartItemSerializer(cart_items, many=True, context={'request': request})

        return Response({
            "cart_items": serializer.data,
            "total_quantity": total_quantity
        }, status=status.HTTP_200_OK)


class CartItemDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, cart__customer=request.user.customer, pk=pk)
        cart_item.delete()
        return Response({"message": "Product successfully deleted from cart"}, status=status.HTTP_200_OK)


# Order Views
class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        orders = Order.objects.filter(customer=customer)
        message = "No orders available" if not orders else "Orders retrieved successfully"
        serializer = OrderSerializer(orders, many=True)
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        data = request.data

        shipping_address = get_object_or_404(ShippingAddress, id=data.get('shipping_address'), customer=customer)
        items = data.get('items', [])

        if not items:
            return Response({"message": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = data.get('payment_method')
        total_amount = data.get('total_amount')
        # item_price = data.get('item_price')

        if payment_method not in ['Online', 'COD']:
            return Response({"message": "Invalid payment method"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(customer=customer, total_amount=total_amount,
                                         shipping_address=shipping_address, payment_method=payment_method)

            for item_data in items:
                product = get_object_or_404(Product, id=item_data.get('product'))
                OrderItem.objects.create(order=order, warehouse=product.warehouse, product=product,
                                         quantity=item_data.get('quantity'), item_price=item_data.get('item_price'))

        return Response({'message': 'Order created successfully', 'order': OrderSerializer(order).data},
                        status=status.HTTP_201_CREATED)


class OrderRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_order(self, order_id, customer):
        return get_object_or_404(Order, id=order_id, customer=customer)

    def get(self, request, order_id):
        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        order = self.get_order(order_id, request.user.customer)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, order_id):
        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        order = self.get_order(order_id, customer)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, order_id):
        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")

        order = self.get_order(order_id, customer)
        order.delete()
        return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Payment Views
class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            customer = self.request.user.customer
        except AttributeError:
            raise NotFound("Authenticated user is not a customer.")
        order_id = request.data.get('order')

        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id)
        payment_method = request.data.get('payment_method')

        if payment_method not in ['Online', 'COD']:
            return Response({'error': 'Invalid payment method'}, status=status.HTTP_400_BAD_REQUEST)

        if payment_method == 'Online':
            return self.process_online_payment(request, customer, order)
        else:
            return self.process_cash_payment(customer, order)

    def process_online_payment(self, request, customer, order):
        amount = request.data.get('amount')
        razorpay_payment_id = request.data.get('razorpay_payment_id')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            payment_order = client.order.create({
                'amount': int(amount) * 100,
                'currency': 'INR',
                'payment_capture': '1',
                'notes': {
                    'name': customer.name,
                    'mobile_number': customer.phone,
                    'amount': amount,
                    'currency': 'INR',
                    'razorpay_payment_id': razorpay_payment_id
                }
            })
            if payment_order.get('status') == 'created':
                Payment.objects.create(
                    customer=customer,
                    order=order,
                    razorpay_order_id=payment_order.get('id'),
                    razorpay_payment_id=razorpay_payment_id,
                    amount=amount,
                    payment_status="Completed",
                    razorpay_payment_status=payment_order.get('status'),
                    payment_method='Online'
                )
                return Response({
                    'message': 'Payment initiated successfully',
                    'razorpay_order_id': payment_order.get('id'),
                    'amount': amount,
                    'currency': 'INR',
                })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_cash_payment(self, customer, order):
        amount = request.data.get('amount')
        Payment.objects.create(
            customer=customer,
            order=order,
            amount=amount,
            payment_status="Completed",
            payment_method='COD'
        )
        return Response({'message': 'Cash payment initiated successfully', 'amount': amount},
                        status=status.HTTP_201_CREATED)


