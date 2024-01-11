from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.utils import swagger_auto_schema

from apps.user.api.serializers.user import (
    AuthenticationSerializer,
    LoginSerializer,
    OtpSerializer,
    RefreshTokenSerializer,
    ChangePasswordSerializer,
    PasswordSerializer,
    ResetPasswordSerializer,
)
from user.api.utils.send_otp import send_otp
from user.api.exceptions import Forbidden
from user.models import BlockedEmail

from config.extensions.utils import get_client_ip


class RegisterView(APIView):
    """
    post:
        Send email for Register.

        parameters: [email]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['api.v1 auth'],
        request_body=AuthenticationSerializer,
        responses={201: AuthenticationSerializer},
    )
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]

            user_is_exists: bool = get_user_model().objects.filter(email=email).values("email").exists()
            if user_is_exists:
                return Response(
                    {
                        "message": _("User exists with this email. Please enter a different email."),
                        "error_code": "user_exists",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            email_blocked: bool = BlockedEmail.objects.filter(email=email).exists()
            if email_blocked:
                raise Forbidden("blockedEmail", 403)

            # The otp code is sent to the user's email for authentication
            return send_otp(request, email)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    """
    post:
        Send email, password for Login.

        parameters: [email, password]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['api.v1 auth'],
        request_body=LoginSerializer,
        responses={201: LoginSerializer},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")

            if not get_user_model().objects.filter(email=email).exists():
                return Response(
                    {"message": _("No User exists with this email. Please enter another email."), },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user = authenticate(email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                context = {
                    "id": user.id,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "is_staff": user.is_staff
                }
                return Response(context, status=status.HTTP_200_OK)

            return Response(
                {"message": _("Email or password is incorrect, please check and try again."), },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyOtpView(APIView):
    """
    post:
        Send otp code to verify EMAIL and complete authentication.

        parameters: [otp,]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "verify_authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['api.v1 auth'],
        request_body=OtpSerializer,
        responses={201: OtpSerializer},
    )
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            received_code = serializer.data.get("code")
            ip = get_client_ip(request)
            email = cache.get(f"{ip}-for-authentication")
            otp = cache.get(email)

            if otp is not None:
                if otp == received_code:
                    user = get_user_model().objects.create(email=email)

                    refresh = RefreshToken.for_user(user)
                    cache.delete(email)
                    cache.delete(f"{ip}-for-authentication")

                    context = {
                        "id": user.id,
                        "created": True,
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


class CreatePasswordView(APIView):
    """
    post:
        Send a password.

        parameters: [password, confirm_password]
    """

    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(
        tags=['api.v1 auth'],
        request_body=PasswordSerializer,
        responses={201: PasswordSerializer},
    )
    def post(self, request):
        if not request.user.two_step_password:
            serializer = PasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            password = serializer.data.get("password")

            try:
                __: None = validate_password(password)
            except ValidationError as err:
                return Response(
                    {"message": err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user = get_object_or_404(get_user_model(), pk=request.user.pk)
            user.set_password(password)
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


class ChangePasswordView(APIView):
    """
    post:
        Send a new password to change a curront password.

        parameters: [old_password, new_password, confirm_new_password,]
    """

    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(
        tags=['api.v1 auth'],
        request_body=ChangePasswordSerializer,
        responses={201: ChangePasswordSerializer},
    )
    def post(self, request):
        if request.user.two_step_password:
            serializer = ChangePasswordSerializer(data=request.data)
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


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer

    @swagger_auto_schema(tags=['api.v1 auth'])
    def post(self, request):
        return super(RefreshTokenView, self).post(request)


class EmailForRPView(RegisterView):
    """
    post:
        Send email to reset password.

        parameters: [email]
    """

    @swagger_auto_schema(
        tags=['api.v1 auth'],
        request_body=AuthenticationSerializer,
        responses={201: AuthenticationSerializer},
    )
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")

            if get_user_model().objects.filter(email=email).exists():
                # The otp code is sent to the user's email for authentication
                return send_otp(request, email)

            return Response(
                {"message": _("User did not found with this email. Please try a different email."), },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordView(APIView):
    """
    post:
        Send otp code to verify EMAIL and complete authentication.

        parameters: [otp,]
    """

    permission_classes = [AllowAny,]
    throttle_scope = "verify_authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['api.v1 auth'],
        request_body=ResetPasswordSerializer,
        responses={201: ResetPasswordSerializer},
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            received_code = serializer.data.get("code")
            password = serializer.data.get("password")
            user_email = serializer.data.get('email')

            ip = get_client_ip(request)
            email = cache.get(f"{ip}-for-authentication")

            if email != user_email:
                return Response({
                    "message": _("Email doesn't match with otp code."),
                    "error_code": "email_dismatches"
                }, status.HTTP_403_FORBIDDEN)

            otp = cache.get(email)

            if otp is not None:
                if otp == received_code:
                    user = get_object_or_404(get_user_model(), email=email)
                    user.set_password(password)
                    user.save(update_fields=['password'])

                    cache.delete(email)
                    cache.delete(f"{ip}-for-authentication")

                    return Response(
                        {"message": _("Password changed successfully")},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {"message": _("Incorrect otp code."), },
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
