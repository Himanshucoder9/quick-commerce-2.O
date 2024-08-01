from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .otp_generator import *
from .models import *
from .serializers import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from App.settings import TEMPLATES_BASE_URL
from django.utils import timezone
from .send_sms import *
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
import datetime
from rest_framework.permissions import IsAuthenticated
from Vendor.serializers import *
from Delivery.serializers import *
# from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CustomerRegisterView(APIView):
    @extend_schema(
        request=CustomerRegisterSerializer,
        responses={200: UserSerializer, 400: 'Invalid credentials'},
        description="Endpoint for user authentication"
    )
    def post(self, request):
        data = request.data
        serializer = CustomerRegisterSerializer(data=data)
        email = data.get('email')
        if serializer.is_valid():
            user = User(
                email=email,
                name=data['name'],
                phone=data['phone'],
                role='CU',
                is_active=False,
                is_verified=False,
            )
            user.set_password(data['password'])   
            user.save()

            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)
            
            send_otp_customer(user, otp)

            if email:
                send_otp_email_customer(user, otp)

            return Response({'message': 'User registered and OTP sent successfully !',
                            'OTP': otp},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        entered_otp = request.data.get('otp')

        try:
            # Check if there is a valid OTP for the entered phone number
            otp_obj = OTP.objects.get(user__phone=phone, otp=entered_otp)
        except OTP.DoesNotExist:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the OTP has expired (more than 10 minutes old)
        if (timezone.now() - otp_obj.timestamp).seconds > 600:
            return Response({'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # Now that we have a valid OTP, mark the user as verified
        user = otp_obj.user
        user.is_active = True
        user.is_verified = True
        user.save()
        
        # Delete the OTP object after successful verification
        otp_obj.delete()

        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)


class ResendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')

        try:
            user = User.objects.get(phone=phone)

            if user.is_verified:
                return Response({'message': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

            otp = generate_otp()

            try:
                existing_otp = OTP.objects.get(user=user)
                existing_otp.delete()
            except OTP.DoesNotExist:
                pass

            OTP.objects.create(user=user, otp=otp)

            send_otp_customer(user, otp)

            return Response({'message': 'New OTP sent successfully.', 'otp': otp}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={200: UserSerializer, 400: 'Invalid credentials'},
        description="Endpoint for user authentication"
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'detail': 'User not found !'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(phone=phone, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            
            return Response({
                'message': 'User login successfully!',
                'token': token.key,
                'user': user_data
            })

        else:
            return Response({'detail': 'Invalid credentials !'}, status=status.HTTP_400_BAD_REQUEST)



class ProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Retrieve user details
        user_data = UserSerializer(user, context={'request': request}).data
        
        # Add role-specific details if applicable
        if user.role == User.VENDOR:
            try:
                vendor = VendorShop.objects.get(user=user)
                vendor_data = VendorSerializer(vendor).data
                user_data['vendor'] = vendor_data
            except VendorShop.DoesNotExist:
                pass

        elif user.role == User.CUSTOMER:
            try:
                customer = Customer.objects.get(user=user)
                customer_data = CustomerSerializer(customer, ).data
                user_data['customer'] = customer_data
            except Customer.DoesNotExist:
                pass

        elif user.role == User.DRIVER:
            try:
                driver = Driver.objects.get(user=user)
                driver_data = DriverSerializer(driver).data
                user_data['driver'] = driver_data
            except Driver.DoesNotExist:
                pass
        return Response(user_data)
    
    # def put(self, request):
    #     return self._update_user(request, partial=False)

    def patch(self, request):
        return self._update_user(request, partial=True)

    def _update_user(self, request, partial):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message":"Profile Updated Successfully",
                "data":serializer.data
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Phone number is required!'}, status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, phone=phone)
        return send_password_reset_sms(user)
        user = User.objects.filter(phone=phone).first()
        if user:
            send_otp(phone)
            return Response({'message': 'New link sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetFormAPIView(APIView):
    def get(self, request, phone, token):
        token_instance = PasswordResetToken.objects.filter(user__phone=phone, token=token).first()
        if token_instance:
            if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
                return Response({
                    "phone": phone,
                    "token": token,
                    "base_url": TEMPLATES_BASE_URL
                })
            else:
                token_instance.delete()
                return Response({"error": "Reset link has expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            token = serializer.validated_data.get('token')
            password = serializer.validated_data.get('password')
            confirm_password = serializer.validated_data.get('confirm_password')
            token_instance = PasswordResetToken.objects.filter(user__phone=phone, token=token).first()

            if token_instance:
                if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
                    try:
                        validate_password(password, user=token_instance.user)

                        if password == confirm_password:
                            user = token_instance.user
                            user.password = make_password(password)
                            user.save()
                            token_instance.delete()
                            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": "Password and confirm password didn't match"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    except ValidationError as e:
                        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    token_instance.delete()
                    return Response({"error": "Reset link has expired"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
