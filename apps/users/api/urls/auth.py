from django.urls import path
from apps.user.api.views.auth import (
    LoginView, RegisterView, VerifyOtpView,
    RefreshTokenView,
    ChangePasswordView, CreatePasswordView,
    EmailForRPView, ResetPasswordView
)


app_name = "auth"


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/", VerifyOtpView.as_view(), name="verify-otp"),
    path("refresh-token/", RefreshTokenView.as_view(), name='refresh-token'),
    path("create-password/", CreatePasswordView.as_view(), name="create-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("reset-password-email/", EmailForRPView.as_view(), name="reset-password-email"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
