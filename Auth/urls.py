from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    # path('vendor/login/', VendorLoginView.as_view()),
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('profile/', ProfileViewSet.as_view(), name='profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-form/<phone>/<token>/', PasswordResetFormAPIView.as_view(), name='password-reset-form'),
    path('password-reset-confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
]