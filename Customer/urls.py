from django.urls import path
from rest_framework.routers import DefaultRouter
from Customer.views import (
    ShippingAddressListCreateAPIView,
    ShippingAddressRetrieveUpdateDestroyAPIView,
    FavoriteViewSet,
    CartRetrieveAPIView,
    CartAddProductAPIView,
    CartItemDeleteAPIView,
    OrderListCreateAPIView,
    OrderRetrieveUpdateDeleteAPIView,
    PaymentAPIView,
)

# Set up the router for FavoriteViewSet
router = DefaultRouter()
router.register(r'favorites', FavoriteViewSet, basename='favorites')

# Define urlpatterns
urlpatterns = [
    # Shipping Address URLs
    path('shipping-address/', ShippingAddressListCreateAPIView.as_view(), name='shipping-addresses'),
    path('shipping-address/<int:pk>/', ShippingAddressRetrieveUpdateDestroyAPIView.as_view(), name='shipping-address'),

    # Cart URLs
    path('cart/add/', CartAddProductAPIView.as_view(), name='cart-add'),
    path('cart/', CartRetrieveAPIView.as_view(), name='cart-list'),
    path('cart/delete/<int:pk>/', CartItemDeleteAPIView.as_view(), name='cart-delete'),

    # Order URLs
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:order_id>/', OrderRetrieveUpdateDeleteAPIView.as_view(), name='order-retrieve-update-delete'),

    # Payment URL
    path('payment/', PaymentAPIView.as_view(), name='payment'),
]

# Include the router's URLs in urlpatterns
urlpatterns += router.urls
