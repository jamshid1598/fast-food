from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema

from users.api.serializers.users import (
    AuthenticationSerializer,
    OtpSerializer,
    CustomTokenRefreshSerializer,
)
from users.api.utils.send_otp import send_otp
from config.extensions.utils import get_client_ip


class Login(APIView):
    """
    post:
        Send mobile number for Login.

        parameters: [phone,]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @extend_schema(tags=['api.v1 otp auth'], request=AuthenticationSerializer, responses={200: AuthenticationSerializer})
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")

            user_is_exists: bool = get_user_model().objects.filter(phone=received_phone).values("phone").exists()
            if not user_is_exists:
                return Response(
                    {"message": _("No User exists with this phone number. Please enter another phone number."),},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # The otp code is sent to the user's phone number for authentication
            return send_otp(request, phone=received_phone)

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,
            )


class Register(APIView):
    """
        POST request: Send mobile number for Register.

        parameters: [phone]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @extend_schema(tags=['api.v1 otp auth'], request=AuthenticationSerializer, responses={201: AuthenticationSerializer})
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")
 
            user_is_exists: bool = get_user_model().objects.filter(phone=received_phone).values("phone").exists()
            if user_is_exists:
                return Response(
                    {"message": _("User exists with this phone number. Please enter a different phone number."),},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # The otp code is sent to the user's phone number for authentication
            return send_otp(request, phone=received_phone)

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,               
            )


class VerifyOtp(APIView):
    """
    post:
        Send otp code and password to verify mobile number and complete authentication.

        parameters: [otp,]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "verify_authentication"
    throttle_classes = [ScopedRateThrottle,]

    @extend_schema(tags=['api.v1 otp auth'], request=OtpSerializer, responses={200: OtpSerializer})
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            received_code = serializer.data.get("code")
            ip = get_client_ip(request)
            phone = cache.get(f"{ip}-for-authentication")
            otp = cache.get(phone)

            if otp is not None:
                if otp == received_code:
                    user, created = get_user_model().objects.get_or_create(phone=phone)
                    if created:
                        user.set_unusable_password()
                        user.save()

                    refresh = RefreshToken.for_user(user)
                    cache.delete(phone)
                    cache.delete(f"{ip}-for-authentication")

                    context = {
                        "id": user.id,
                        "created": created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": _("Incorrect code."),},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {"message": _("The entered code has expired."),},
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(tags=['api.v1 otp auth'])
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
