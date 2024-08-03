from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('warehouse/register/', WarehouseRegisterView.as_view(), name='warehouse-register'),
    path('driver/register/', DriverRegisterView.as_view(), name='driver-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('warehouse/profile/', WarehouseProfileView.as_view(), name='warehouse-profile'),
    path('driver/profile/', DriverProfileView.as_view(), name='driver-profile'),
]