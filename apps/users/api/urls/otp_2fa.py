from django.urls import path
from apps.user.api.views.otp_2fa import (
    Login, Register, VerifyOtp,
    VerifyTwoStepPassword, ChangeTwoStepPassword, CreateTwoStepPassword,
    CustomTokenRefreshView,
)


app_name = "otp_2fa"


urlpatterns = [
    # otp with two factor authentication
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("verify/", VerifyOtp.as_view(), name="verify-otp"),
    path("refresh-token/", CustomTokenRefreshView.as_view(), name='refresh-token'),
    path("create-two-step-password/", CreateTwoStepPassword.as_view(), name="create-two-step-password"),
    path("verify-two-step-password/", VerifyTwoStepPassword.as_view(), name="verify-two-step-password"),
    path("change-two-step-password/", ChangeTwoStepPassword.as_view(), name="change-two-step-password"),
]
