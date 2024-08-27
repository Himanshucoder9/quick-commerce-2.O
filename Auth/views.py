from rest_framework.views import APIView
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import PermissionDenied
from django.http import Http404
from Auth.otp_generator import generate_otp, verify_otp, verify_profile_delete_otp
from Auth.models import User, Customer, WareHouse, OTP, Driver, ForgetOTP
from Auth.serializers import (
    CustomerRegisterSerializer, CustomerProfileSerializer,
    LoginSerializer, WareHouseRegisterSerializer,
    WareHouseProfileSerializer, DriverRegisterSerializer,
    DriverProfileSerializer
)
from Notification.phone_sms import (
    send_customer_register_otp, send_warehouse_register_otp
)
from Notification.email_notification import (
    send_customer_register_email_otp, send_warehouse_register_email_otp
)


# Create a base class for user registration with common functionality
class UserRegisterView(APIView):
    def create_user(self, serializer_class, role):
        serializer = serializer_class(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save(role=role, is_active=False)
            user.set_password(self.request.data.get('password'))
            user.save()
            return user, serializer
        return None, serializer.errors

    def create_otp(self, user):
        otp = generate_otp()
        OTP.objects.create(user=user, otp=otp)
        return otp


class CustomerRegisterView(UserRegisterView):
    @extend_schema(
        request=CustomerRegisterSerializer,
        responses={201: CustomerProfileSerializer, 400: 'Invalid credentials'},
        description="Endpoint for user registration and OTP sending"
    )
    def post(self, request):
        user, errors = self.create_user(CustomerRegisterSerializer, role='CU')
        if user:
            otp = self.create_otp(user)
            send_customer_register_otp(user, otp)
            if user.email:
                send_customer_register_email_otp(user, otp)
            return Response({
                'message': 'User registered and OTP sent successfully!',
                'OTP': otp
            }, status=status.HTTP_201_CREATED)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        entered_otp = request.data.get('otp')

        try:
            otp_obj = OTP.objects.get(user__phone=phone, otp=entered_otp)
        except OTP.DoesNotExist:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        if (timezone.now() - otp_obj.created_at) > timezone.timedelta(minutes=10):
            otp_obj.delete()
            return Response({'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user = otp_obj.user
        if user.is_active:
            otp_obj.delete()
            return Response({'message': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        otp_obj.delete()
        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)


class ResendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'message': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        OTP.objects.update_or_create(user=user, defaults={'otp': otp})
        # Uncomment to send OTP via SMS or email
        # send_otp_customer(user, otp)
        return Response({'message': 'New OTP sent successfully.', 'OTP': otp}, status=status.HTTP_200_OK)


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={200: CustomerProfileSerializer, 400: 'Invalid credentials'},
        description="Endpoint for user authentication"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'detail': 'User not found!'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'detail': 'User is not verified!'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(phone=phone, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = CustomerProfileSerializer(user).data

            return Response({
                'message': 'User login successfully!',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data
            })
        return Response({'detail': 'Invalid credentials!'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', ]

    def get_object(self):
        user = self.request.user
        if self.queryset.model == User:
            return user

        model_instance = self.queryset.model.objects.filter(id=user.id).first()
        if not model_instance:
            raise Http404(f"{self.queryset.model.__name__} profile does not exist.")
        return model_instance

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Profile updated successfully!',
            'profile': serializer.data
        }, status=status.HTTP_200_OK)


class CustomerProfileView(UserProfileView):
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer


class WarehouseRegisterView(UserRegisterView):
    @extend_schema(
        request=WareHouseRegisterSerializer,
        responses={201: WareHouseProfileSerializer, 400: 'Invalid credentials'},
        description="Endpoint for warehouse registration and OTP sending"
    )
    def post(self, request):
        user, errors = self.create_user(WareHouseRegisterSerializer, role='WH')
        if user:
            otp = self.create_otp(user)
            send_warehouse_register_otp(user, otp)
            if user.email:
                send_warehouse_register_email_otp(user, otp)
            return Response({
                'message': 'Warehouse registered and OTP sent successfully!',
                'OTP': otp
            }, status=status.HTTP_201_CREATED)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)



class WarehouseProfileView(UserProfileView):
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseProfileSerializer

    def get_object(self):
        user = self.request.user
        if user.role != 'WH':
            raise PermissionDenied("Authenticated user is not a warehouse user.")
        return super().get_object()


class DriverRegisterView(UserRegisterView):
    @extend_schema(
        request=DriverRegisterSerializer,
        responses={201: DriverProfileSerializer, 400: 'Invalid credentials'},
        description="Endpoint for driver registration and OTP sending"
    )
    def post(self, request):
        user, errors = self.create_user(DriverRegisterSerializer, role='DR')
        if user:
            otp = self.send_otp(user)
            return Response({
                'message': 'Driver registered and OTP sent successfully!',
                'OTP': otp
            }, status=status.HTTP_201_CREATED)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)


class DriverProfileView(UserProfileView):
    queryset = Driver.objects.all()
    serializer_class = DriverProfileSerializer

    def get_object(self):
        user = self.request.user
        if user.role != 'DR':
            raise PermissionDenied("Authenticated user is not a driver user.")
        return super().get_object()


class PasswordResetRequestView(APIView):
    def post(self, request):
        phone = request.data.get('phone')

        if not phone:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'No user found with this phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        # send_otp_to_phone(user.phone, otp)
        ForgetOTP.objects.update_or_create(
            user=user,
            defaults={'otp': otp, 'created_at': timezone.now()}
        )

        return Response({'message': 'OTP sent to your phone.', 'OTP': otp}, status=status.HTTP_200_OK)


class PasswordResetVerifyView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not phone or not otp or not new_password:
            return Response({'error': 'Phone number, OTP, and new password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'No user found with this phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_otp(user, otp):
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)


class ProfileDeleteRequestView(APIView):
    def post(self, request):
        phone = request.data.get('phone')

        if not phone:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'No user found with this phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        # send_otp_to_phone(user.phone, otp)
        OTP.objects.update_or_create(
            user=user,
            defaults={'otp': otp, 'created_at': timezone.now()}
        )

        return Response({'message': 'OTP sent to your phone number for delete profile.', 'OTP': otp},
                        status=status.HTTP_200_OK)


class ProfileDeleteVerifyView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        if not phone or not otp:
            return Response({"detail": "Phone number and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({"detail": "No user found with this phone number."}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_profile_delete_otp(user, otp):
            return Response({"detail": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"detail": "User profile deleted successfully."}, status=status.HTTP_200_OK)


class UpdateDeviceTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        device_token = request.data.get("device_token")

        if not device_token:
            return Response({"error": "Device token is required."}, status=status.HTTP_400_BAD_REQUEST)

        user.device_token = device_token
        user.save()

        return Response({"message": "Device token updated successfully."}, status=status.HTTP_200_OK)
