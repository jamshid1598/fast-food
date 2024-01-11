from django.urls import path, include

from user.api.views.user import (
    UsersList, UserDetailUpdateDelete,
    UserProfile, DeleteAccount, UserFcmTokenView
)
from user.api.views.otp_status import OTPStatusView

from user.api.views.profile import ProfileImageAPI, ProfileImageDetailAPI, ProfileMainImageAPI
from user.api.views.filter_options import SetFilterOptionsAPI
from user.api.views.filter_users import (
    FilterUsersAPI, FilterUserAPI,
    ReactionAPI, ReactionEditDeleteAPI, MyLikesAPI, LikesAPI,
    MyBlocksAPI, SearchUserAPI,
)

app_name = "api"

urlpatterns = [
    path("", UsersList.as_view(), name="users-list"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("profile/images/", ProfileImageAPI.as_view(), name="profile-images"),
    path("profile/set-main-image/", ProfileMainImageAPI.as_view(), name="profile-set-main-image"),
    path("profile/images/<int:pk>/", ProfileImageDetailAPI.as_view(), name="profile-image-detail"),
    path("delete-account/", DeleteAccount.as_view(), name="delete-account"),
    path("user/<uuid:pk>/", UserDetailUpdateDelete.as_view(), name="user-detail"),
    path("user-fcm_token/", UserFcmTokenView.as_view(), name="user-fcm-token"),
    path("opt-status/", OTPStatusView.as_view(), name="opt-status"),

    path("filters/filter-options/", SetFilterOptionsAPI.as_view(), name='filter-options'),
    path("filters/users/", FilterUsersAPI.as_view(), name='filter-users'),
    path("search/users/", SearchUserAPI.as_view(), name='search-users'),
    path("filters/user-detail/", FilterUserAPI.as_view(), name='filter-user-detail'),

    path("reactions/", ReactionAPI.as_view(), name='reaction-create'),
    path("reactions/<int:pk>/", ReactionEditDeleteAPI.as_view(), name='reaction-edit-delete'),

    path("my-likes/", MyLikesAPI.as_view(), name='my-likes'),
    path("my-blocked-users/", MyBlocksAPI.as_view(), name='my-blocked-users'),
    path("likes/", LikesAPI.as_view(), name='likes'),

    path("admins/", include("user.api.urls.admin")),

    # otp authentication
    path("", include("user.api.urls.auth", namespace="auth")),

    # otp with two factor authentication
    # path("2fa/", include("user.api.urls.otp_2fa", namespace="otp_2fa")),
]
