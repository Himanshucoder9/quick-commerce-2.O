from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    CustomerRegisterView,
    WarehouseRegisterView,
    DriverRegisterView,
    VerifyOTPView,
    ResendOTPView,
    CustomerProfileView,
    WarehouseProfileView,
    DriverProfileView,
)

urlpatterns = [
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User registration endpoints
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('warehouse/register/', WarehouseRegisterView.as_view(), name='warehouse-register'),
    path('driver/register/', DriverRegisterView.as_view(), name='driver-register'),

    # OTP management endpoints
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),

    # Profile endpoints
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('warehouse/profile/', WarehouseProfileView.as_view(), name='warehouse-profile'),
    path('driver/profile/', DriverProfileView.as_view(), name='driver-profile'),
]
