from rest_framework.views import APIView
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from Auth.otp_generator import *
from Auth.models import User, Customer, WareHouse, OTP
from Auth.serializers import *
from Auth.send_sms import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateAPIView
from django.core.exceptions import PermissionDenied
from django.http import Http404


# from Warehouse.serializers import *
# from Delivery.serializers import *


class CustomerRegisterView(APIView):
    @extend_schema(
        request=CustomerRegisterSerializer,
        responses={201: CustomerProfileSerializer, 400: 'Invalid credentials'},
        description="Endpoint for user registration and OTP sending"
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
            )
            user.set_password(data['password'])
            user.save()

            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)

            # send_otp_customer(user, otp)

            # if email:
            #     send_otp_email_customer(user, otp)

            return Response({
                'message': 'User registered and OTP sent successfully!',
                'OTP': otp
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


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
        # send_otp_customer(user, otp)

        return Response({'message': 'New OTP sent successfully.', 'OTP': otp}, status=status.HTTP_200_OK)


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={200: CustomerProfileSerializer, 400: 'Invalid credentials'},
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
        
        if not user.is_active:
            return Response({'detail': 'User is not verified !'}, status=status.HTTP_400_BAD_REQUEST)

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

        else:
            return Response({'detail': 'Invalid credentials !'}, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Profile updated successfully!',
            'profile': serializer.data
        }, status=status.HTTP_200_OK)


class WarehouseRegisterView(APIView):
    @extend_schema(
        request=WareHouseRegisterSerializer,
        responses={201: WareHouseProfileSerializer, 400: 'Invalid credentials'},
        description="Endpoint for user registration and OTP sending"
    )
    def post(self, request):
        serializer = WareHouseRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            warehouse = serializer.save(
                role='WH',
                is_active=False
            )
            warehouse.set_password(request.data.get('password'))
            warehouse.save()

            otp = generate_otp()
            OTP.objects.create(user=warehouse, otp=otp)

            # if warehouse.email:
            #     send_otp_email_customer(warehouse, otp)

            return Response({
                'message': 'Warehouse registered and OTP sent successfully!',
                'OTP': otp
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


class WarehouseProfileView(RetrieveUpdateAPIView):
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        if user.role == 'WH':
            try:
                return WareHouse.objects.get(id=user.id)
            except WareHouse.DoesNotExist:
                raise Http404("Warehouse profile does not exist.")
        else:
            raise PermissionDenied("Authenticated user is not a warehouse user.")

    def perform_update(self, serializer):
        serializer.save()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Profile updated successfully!',
            'profile': serializer.data
        }, status=status.HTTP_200_OK)



class DriverRegisterView(APIView):
    @extend_schema(
        request=DriverRegisterSerializer,
        responses={201: DriverProfileSerializer, 400: 'Invalid credentials'},
        description="Endpoint for user registration and OTP sending"
    )
    def post(self, request):
        serializer = DriverRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            driver = serializer.save(
                role='DR',
                is_active=False
            )
            driver.set_password(request.data.get('password'))
            driver.save()

            otp = generate_otp()
            OTP.objects.create(user=driver, otp=otp)

            # if driver.email:
            #     send_otp_email_customer(warehouse, otp)

            return Response({
                'message': 'Driver registered and OTP sent successfully!',
                'OTP': otp
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


class DriverProfileView(RetrieveUpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        if user.role == 'DR':
            try:
                return Driver.objects.get(id=user.id)
            except Driver.DoesNotExist:
                raise Http404("Driver profile does not exist.")
        else:
            raise PermissionDenied("Authenticated user is not a driver user.")

    def perform_update(self, serializer):
        serializer.save()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Profile updated successfully!',
            'profile': serializer.data
        }, status=status.HTTP_200_OK)

