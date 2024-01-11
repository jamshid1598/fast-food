from django.urls import path

from user.api.views.admin.users import (
    UserAPI, UserDetailAPI,
    BlockUserAPI, BlockUserDetailAPI,
    UserProfileMainImageAPI, ProfileImageCreateAPI, ProfileImageDeleteAPI,
)
from user.api.views.admin.user_filter_options import UserFilterOptionsAPI

app_name = 'admin-actions'

urlpatterns = [
    path('users/', UserAPI.as_view(), name='users-list-create'),
    path('users/detail/<uuid:pk>/', UserDetailAPI.as_view(), name='user-detail-update-delete'),
    path('block-users/', BlockUserAPI.as_view(), name='blockeds-list-create'),
    path('block-user/<int:pk>/', BlockUserDetailAPI.as_view(), name='block-user'),
    path('user/filter-options/<uuid:pk>/', UserFilterOptionsAPI.as_view(), name='user-filter-options'),

    path('users/profile/set-main-image/<uuid:pk>/', UserProfileMainImageAPI.as_view(), name='admin-set-main-image'),
    path('users/profile/images/create/', ProfileImageCreateAPI.as_view(), name='admin-create-profile-image'),
    path('users/profile/images/delete/<int:pk>/', ProfileImageDeleteAPI.as_view(), name='admin-delete-profile-image'),
]
