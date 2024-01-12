from django.urls import path

from users.api.views.users import (
    UsersList, UserDetailUpdateDelete,
    UserProfile, DeleteAccount
)
from users.api.views.auth import (
    Login, Register, VerifyOtp,
    CustomTokenRefreshView,
)

from users.api.views.otp_status import OTPStatusView


app_name = "api"

urlpatterns = [
    path("", UsersList.as_view(), name="users-list"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("delete-account/", DeleteAccount.as_view(), name="delete-account"),
    path("user/<uuid:pk>/", UserDetailUpdateDelete.as_view(), name="user-detail"),
    path("opt-status/", OTPStatusView.as_view(), name="opt-status"),

    # otp authentication
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("verify/", VerifyOtp.as_view(), name="verify-otp"),
    path("refresh-token/", CustomTokenRefreshView.as_view(), name='refresh-token'),
]
