from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    # path('vendor/login/', VendorLoginView.as_view()),
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('profile/', ProfileViewSet.as_view(), name='profile'),
]