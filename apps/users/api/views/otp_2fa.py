from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema

from apps.user.api.serializers.user import (
    AuthenticationSerializer,
    PhoneEmailSerializer,
    OtpSerializer,
    ChangeTwoStepPasswordSerializer,
    GetTwoStepPasswordSerializer,
    CustomTokenRefreshSerializer,
)
from user.api.utils.send_otp import send_otp
from config.extensions.utils import get_client_ip, username_generator


class Login(APIView):
    """
    post:
        Send mobile-number or email for Login.

        parameters: [phone_email]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['api.v1 otp-2fa auth'],
        request_body=AuthenticationSerializer,
        responses={201: AuthenticationSerializer},
    )
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            phone_email = serializer.data.get("phone_email")

            if phone_email.isdigit():
                PhoneEmailSerializer(data={'phone': phone_email}).is_valid(raise_exception=True)
                user_is_exists: bool = get_user_model().objects.filter(phone=phone_email).values("phone").exists()
            else:
                PhoneEmailSerializer(data={'email': phone_email}).is_valid(raise_exception=True)
                user_is_exists: bool = get_user_model().objects.filter(email=phone_email).values("email").exists()

            if not user_is_exists:
                msg = _("No User exists with this %s.") % phone_email
                return Response(
                    {"message": msg, }, status=status.HTTP_401_UNAUTHORIZED,
                )

            # The otp code is sent to the user's phone number for authentication
            return send_otp(request, phone_email)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class Register(APIView):
    """
    post:
        Send `phone-number` or `email` for Register.

        parameters: [phone_email]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['api.v1 otp-2fa auth'],
        request_body=AuthenticationSerializer,
        responses={201: AuthenticationSerializer},
    )
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            phone_email = serializer.data.get("phone_email")

            if phone_email.isdigit():
                PhoneEmailSerializer(data={'phone': phone_email}).is_valid(raise_exception=True)
                # user_is_exists: bool = get_user_model().objects.filter(phone=phone_email).values("phone").exists()
            else:
                PhoneEmailSerializer(data={'email': phone_email}).is_valid(raise_exception=True)
                # user_is_exists: bool = get_user_model().objects.filter(email=phone_email).values("email").exists()

            # if user_is_exists:
            #     return Response(
            #         {"message": _("User exists with this phone number. Please enter a different phone number.")},
            #         status=status.HTTP_401_UNAUTHORIZED,
            #     )

            # The otp code is sent to the user's phone number for authentication
            return send_otp(request, phone_email)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyOtp(APIView):
    """
    post:
        Send otp code to verify mobile number and complete authentication.

        parameters: [otp,]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "verify_authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['api.v1 otp-2fa auth'],
        request_body=OtpSerializer,
        responses={201: OtpSerializer},
    )
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            received_code = serializer.data.get("code")
            received_phone_email = serializer.data.get('phone_email')
            ip = get_client_ip(request)
            phone_email = cache.get(f"{ip}-for-authentication")
            otp = cache.get(phone_email)

            if otp is not None:
                if otp == received_code and received_phone_email == phone_email:
                    if phone_email.isdigit():
                        user, created = get_user_model().objects.get_or_create(phone=phone_email)
                    else:
                        user, created = get_user_model().objects.get_or_create(email=phone_email)

                    if user.two_step_password:
                        cache.set(f"{ip}-for-two-step-password", user, 250)
                        return Response(
                            {"message": _("Thanks, please enter your two-step password")},
                            status=status.HTTP_200_OK,
                        )

                    refresh = RefreshToken.for_user(user)
                    cache.delete(phone_email)
                    cache.delete(f"{ip}-for-authentication")

                    if created:
                        temp_username = username_generator()
                        while get_user_model().objects.filter(username=temp_username).exists():
                            temp_username = username_generator()
                        user.username = temp_username
                        user.save(update_fields=['username'])

                    context = {
                        "created": created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": _("Incorrect code."), },
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {"message": _("The entered code has expired."), },
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyTwoStepPassword(APIView):
    """
    post:
        Send two-step-password to verify and complete authentication.

        parameters: [password, confirm_password,]
    """

    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        tags=['api.v1 otp-2fa auth'],
        request_body=GetTwoStepPasswordSerializer,
        responses={201: GetTwoStepPasswordSerializer},
    )
    def post(self, request):
        serializer = GetTwoStepPasswordSerializer(data=request.data)
        if serializer.is_valid():
            ip = get_client_ip(request)
            user = cache.get(f"{ip}-for-two-step-password")

            if user is not None:
                password = serializer.data.get("password")
                check_password: bool = user.check_password(password)

                if check_password:
                    refresh = RefreshToken.for_user(user)
                    cache.delete(f"{ip}-for-two-step-password")

                    context = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(
                        context,
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": _("The password entered is incorrect")},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            return Response(
                {"message": _("The two-step-password entry time has elapsed")},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateTwoStepPassword(APIView):
    """
    post:
        Send a password to create a two-step-password.

        parameters: [new_password, confirm_new_password]
    """

    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(
        tags=['api.v1 otp-2fa auth'],
        request_body=GetTwoStepPasswordSerializer,
        responses={201: GetTwoStepPasswordSerializer},
    )
    def post(self, request):
        if not request.user.two_step_password:
            serializer = GetTwoStepPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_password = serializer.data.get("password")

            try:
                __: None = validate_password(new_password)
            except ValidationError as err:
                return Response(
                    {"message": err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user = get_object_or_404(get_user_model(), pk=request.user.pk)
            user.set_password(new_password)
            user.two_step_password = True
            user.save(update_fields=["password", "two_step_password"])
            return Response(
                {"message": _("Your password was created successfully."), },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": _("Already created, try to change.")},
            status=status.HTTP_403_FORBIDDEN,
        )


class ChangeTwoStepPassword(APIView):
    """
    post:
        Send a password to change a two-step-password.

        parameters: [old_password, new_password, confirm_new_password,]
    """

    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(
        tags=['api.v1 otp-2fa auth'],
        request_body=ChangeTwoStepPasswordSerializer,
        responses={201: ChangeTwoStepPasswordSerializer},
    )
    def post(self, request):
        if request.user.two_step_password:
            serializer = ChangeTwoStepPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_password = serializer.data.get("password")

            try:
                __: None = validate_password(new_password)
            except ValidationError as err:
                return Response(
                    {"message": err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            old_password = serializer.data.get("old_password")
            check_password: bool = request.user.check_password(old_password)

            if check_password:
                request.user.set_password(new_password)
                request.user.save(update_fields=["password"])

                return Response(
                    {"message": _("Your password was changed successfully.")},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": _("The password entered is incorrect.")},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        return Response(
            {"message": _("Your request could not be approved.")},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    @swagger_auto_schema(tags=['api.v1 otp-2fa auth'])
    def post(self, request):
        return super(CustomTokenRefreshView, self).post(request)
