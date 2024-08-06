from django.urls import path
from Delivery.views import (
    PendingDeliveriesListView,
    DeliveryStatusToPickedUpView,
    DriverDeliveryDetailView,
    DeliveryStatusToInTransitView,
    DeliveryStatusToDeliveredView,
    ResendDeliveryOTPView,
    DeliveryStatusToCancelView,
    DeliveryStatusView,
    DriverAllOrdersAPIView,
    DriverDashboardAPIView,
)

urlpatterns = [
    # Driver dashboard
    path('dashboard/', DriverDashboardAPIView.as_view(), name='driver-dashboard'),

    # Pending deliveries
    path('pending/', PendingDeliveriesListView.as_view(), name='pending-deliveries'),

    # Delivery order details
    path('order/detail/', DriverDeliveryDetailView.as_view(), name='deliveries-order-details'),

    # Delivery status updates
    path('<int:pk>/pick-up/', DeliveryStatusToPickedUpView.as_view(), name='delivery-pick-up'),
    path('<int:pk>/in-transit/', DeliveryStatusToInTransitView.as_view(), name='delivery-in-transit'),
    path('<int:pk>/delivered/', DeliveryStatusToDeliveredView.as_view(), name='delivery-delivered'),
    path('<int:pk>/resend-otp/', ResendDeliveryOTPView.as_view(), name='resend-delivery-otp'),
    path('<int:pk>/cancel/', DeliveryStatusToCancelView.as_view(), name='cancel-delivery'),

    # Driver all orders
    path('all-orders/', DriverAllOrdersAPIView.as_view(), name='driver-all-orders'),

    # Track delivery status
    path('track/<str:order_number>/', DeliveryStatusView.as_view(), name='track-delivery'),
]
