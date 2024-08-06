from datetime import timedelta
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from Auth.models import Driver
from Auth.otp_generator import generate_otp
from Customer.models import Order
from Delivery.models import DeliveryAddress
from Delivery.serializers import DetailDeliverySerializer, DeliverySerializer, DeliveryStatusSerializer, \
    CustomerDeliveryStatusSerializer
import logging

# Create your views here.

logger = logging.getLogger(__name__)


class PendingDeliveriesListView(ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        driver = self.request.user

        pending_deliveries = DeliveryAddress.objects.filter(driver=driver, status='PROCESSING')

        return Order.objects.filter(deliveries__in=pending_deliveries).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No pending deliveries found for this driver."},
                            status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverDeliveryDetailView(RetrieveAPIView):
    serializer_class = DetailDeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        driver = self.request.user
        delivery_id = self.kwargs.get('pk')

        try:
            return DeliveryAddress.objects.get(id=delivery_id, driver=driver)
        except DeliveryAddress.DoesNotExist:
            raise NotFound("Delivery not found for this driver.")

    def get(self, request, *args, **kwargs):
        delivery_address = self.get_object()
        serializer = self.get_serializer(delivery_address)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryStatusToPickedUpView(UpdateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the authenticated user is a driver
        try:
            driver = request.user
            if not isinstance(driver, Driver):
                raise Driver.DoesNotExist
        except Driver.DoesNotExist:
            return Response({"message": "Authenticated user is not a driver"}, status=status.HTTP_403_FORBIDDEN)

        # Check if the driver is associated with the delivery instance
        if instance.driver != driver:
            return Response({"message": "Authenticated user is not assigned to this delivery"},
                            status=status.HTTP_403_FORBIDDEN)

        # Check if the delivery status allows for picking up
        if instance.status == "DELIVERED":
            return Response({"message": "Order is already DELIVERED"}, status=status.HTTP_400_BAD_REQUEST)

        if instance.status == "IN_TRANSIT":
            return Response({"message": "Order is already in transit"}, status=status.HTTP_400_BAD_REQUEST)

        if instance.status == "CANCELLED":
            return Response({"message": "Order is CANCELLED"}, status=status.HTTP_400_BAD_REQUEST)

        # Update delivery status to 'PICKED_UP'
        instance.status = "PICKED_UP"
        instance.save()

        # Update the order status to 'PROCESSING'
        orders = instance.orders.all()  # Get all related orders
        for order in orders:
            order.order_status = "Processing"  # Use the correct status choice
            order.save()

        return Response({"message": "Order status updated to PICKED UP."}, status=status.HTTP_200_OK)


class DeliveryStatusToInTransitView(UpdateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        driver = request.user
        if not hasattr(driver, 'driver_user'):
            return Response({"message": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        instance = self.get_object()

        if instance.driver != driver.driver_user:
            return Response({"message": "Authenticated user is not the assigned driver for this delivery."},
                            status=status.HTTP_403_FORBIDDEN)

        if instance.status == "DELIVERED":
            return Response({"message": "Order is already DELIVERED"}, status=status.HTTP_400_BAD_REQUEST)

        if instance.status == "CANCELLED":
            return Response({"message": "Order is already CANCELLED"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate OTP and update status
        otp = generate_otp()
        instance.otp_created_at = timezone.now()
        instance.status = 'IN_TRANSIT'
        instance.otp = otp

        # Save the instance
        instance.save()

        # Uncomment the following line to send the OTP to the customer
        # send_delivery_otp_customer(instance.orders.first().customer.phone, otp)

        return Response({
            "message": "Order status updated to IN_TRANSIT and OTP sent to the customer.",
            "OTP": otp
        }, status=status.HTTP_200_OK)


class DeliveryStatusToDeliveredView(UpdateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        driver = request.user

        if not hasattr(driver, 'driver_user'):
            return Response({"message": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        instance = self.get_object()

        if instance.driver != driver.driver_user:
            return Response({"message": "Authenticated user is not the assigned driver for this delivery."},
                            status=status.HTTP_403_FORBIDDEN)

        provided_otp = request.data.get('otp')
        logger.error(f"Provided OTP: {provided_otp}, Stored OTP: {instance.otp}")  # Log for debugging

        if not provided_otp:
            return Response({"message": "OTP is required to mark the order as DELIVERED."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the OTP is expired
        if instance.otp_created_at and timezone.now() > instance.otp_created_at + timedelta(minutes=15):
            return Response({"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the provided OTP
        if provided_otp != instance.otp:
            return Response({"message": "Invalid OTP provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the delivery status
        instance.status = 'DELIVERED'
        instance.otp = None  # Clear the OTP once delivered
        instance.otp_created_at = None
        instance.save()

        order = instance.orders.first()
        order.order_status = 'Completed'
        order.save()

        return Response({"message": "OTP verified successfully and Order marked as DELIVERED."},
                        status=status.HTTP_200_OK)


class ResendDeliveryOTPView(UpdateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        driver = request.user

        if not hasattr(driver, 'driver_user'):
            return Response({"message": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        instance = self.get_object()

        if instance.driver != driver.driver_user:
            return Response({"message": "Authenticated user is not the assigned driver for this delivery."},
                            status=status.HTTP_403_FORBIDDEN)

        # Check if the order is already delivered
        if instance.status == "DELIVERED":
            return Response({"message": "Order is already DELIVERED"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a new OTP
        new_otp = generate_otp()
        instance.otp = new_otp
        instance.otp_created_at = timezone.now()
        instance.save()

        # Optionally send the new OTP to the customer
        # send_delivery_otp_customer(instance.order.user.phone, new_otp)

        return Response({"message": "A new Delivery OTP has been sent to the customer.", "OTP": new_otp},
                        status=status.HTTP_200_OK)


class DeliveryStatusToCancelView(UpdateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        driver = request.user

        if not hasattr(driver, 'driver_user'):
            return Response({"message": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        instance = self.get_object()

        if instance.driver != driver.driver_user:
            return Response({"message": "Authenticated user is not the assigned driver for this delivery."},
                            status=status.HTTP_403_FORBIDDEN)

        if instance.status == "DELIVERED":
            return Response({"message": "Order is already DELIVERED"}, status=status.HTTP_400_BAD_REQUEST)

        # Cancel the delivery
        instance.status = "CANCELLED"
        instance.save()

        # Update the order status to 'rejected'
        order = instance.orders.first()
        order.order_status = 'Canceled'
        order.save()

        return Response({"message": "Order marked as CANCELLED"}, status=status.HTTP_200_OK)


class DeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        # Check if the order exists for the authenticated user
        try:
            order = Order.objects.get(order_number=order_number, customer=request.user)
        except Order.DoesNotExist:
            return Response({"message": "Order not found or does not belong to the authenticated user"},
                            status=status.HTTP_404_NOT_FOUND)

        # Check if there is a delivery address related to the order
        try:
            delivery_address = DeliveryAddress.objects.get(orders=order)
        except DeliveryAddress.DoesNotExist:
            return Response({"message": "Delivery information not found for this order"},
                            status=status.HTTP_404_NOT_FOUND)

        # Serialize the delivery address
        serializer = CustomerDeliveryStatusSerializer(delivery_address)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverAllOrdersAPIView(ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        driver = self.request.user
        return Order.objects.filter(deliveryaddress__driver=driver).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No orders assigned to this driver."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        driver = request.user
        today = timezone.now().date()

        todays_orders = Order.objects.filter(deliveryaddress__driver=driver, created_at__date=today).distinct().count()
        total_orders = Order.objects.filter(deliveryaddress__driver=driver).distinct().count()
        processing_orders = Order.objects.filter(deliveryaddress__driver=driver,
                                                 deliveryaddress__status='PROCESSING').distinct().count()
        completed_orders = Order.objects.filter(deliveryaddress__driver=driver,
                                                deliveryaddress__status='DELIVERED').distinct().count()
        canceled_orders = Order.objects.filter(deliveryaddress__driver=driver,
                                               deliveryaddress__status='CANCELLED').count()

        data = {
            "todays_orders": todays_orders,
            "total_orders": total_orders,
            "processing_orders": processing_orders,
            "completed_orders": completed_orders,
            "canceled_orders": canceled_orders
        }

        return Response(data, status=status.HTTP_200_OK)
