from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserType


class IsAdmin(BasePermission):
    message = 'You Must Be Admin'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.user_type == UserType.ADMIN
        )


class IsWaiter(BasePermission):
    message = 'You Must Be Waiter'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.user_type == UserType.WAITER
        )


class IsClient(BasePermission):
    message = 'You Must Be Client'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.user_type == UserType.CLIENT
        )


class IsAdminOrWaiter(BasePermission):
    message = 'You Must Be Admin or Waiter'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.user_type == UserType.ADMIN or
            request.user.is_authenticated and request.user.user_type == UserType.WAITER
        )


class IsAdminOrWaiterOrReadOnly(BasePermission):
    message = 'You Must Be Admin or Waiter'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.user_type == UserType.ADMIN or
            request.user.is_authenticated and request.user.user_type == UserType.WAITER
        )


class IsAdminOrClientOrReadOnly(BasePermission):
    message = 'You Must Be Admin or Client'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.user_type == UserType.ADMIN or
            request.user.is_authenticated and request.user.user_type == UserType.CLIENT
        )


class IsAdminOrWaiterOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.user_type == UserType.ADMIN or
            request.user.is_authenticated and request.user.user_type == UserType.WAITER
        )
