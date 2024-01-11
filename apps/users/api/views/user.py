from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from user.api.serializers.user import (
    UsersListSerializer,
    UserDetailUpdateDeleteSerializer,
    UserProfileSerializer,
    PasswordSerializer,
    UserFcmTokenSerializer,
)
from user.permissions import IsSuperUser
from core.models import Hobby


@extend_schema(tags=['api.v1 users (for admin-panel)'])
class UsersList(ListAPIView):
    """
    get:
        Returns a list of all existing users.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UsersListSerializer
    permission_classes = [IsSuperUser,]
    filterset_fields = ["gender",]
    search_fields = ["phone", "first_name", "last_name",]
    ordering_fields = ("id", "gender",)

    def get_queryset(self):
        return get_user_model().objects.values(
            "id", "phone",
            "first_name", "last_name",
            "gender",
        )


@extend_schema(tags=['api.v1 users (for admin-panel)'])
class UserDetailUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the detail of a user instance.

        parameters: [pk]

    put:
        Update the detail of a user instance

        parameters: exclude[password,]

    delete:
        Delete a user instance.

        parameters: [pk]
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserDetailUpdateDeleteSerializer
    permission_classes = [IsSuperUser,]

    def get_object(self):
        pk = self.kwargs.get("pk")
        user = get_object_or_404(
            get_user_model().objects.defer("password",),
            pk=pk,
        )
        return user


@extend_schema(tags=['api.v1 user-info'])
class UserFcmTokenView(APIView):
    """only `POST` request

    Args:
        `fcm_token` : type string

    Returns:
        success message and status code 202 accepted
    """

    permission_classes = [IsAuthenticated,]

    @extend_schema(
        request=UserFcmTokenSerializer,
        responses={202: None},
        methods=["POST"]
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UserFcmTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fcm_token = serializer.data.get('fcm_token')
        user.fcm_token = fcm_token
        user.save(update_fields=['fcm_token'])
        return Response({"message": _("successfully saved")},
                        status=status.HTTP_202_ACCEPTED)


@extend_schema(tags=['api.v1 user-info'])
class UserProfile(RetrieveUpdateAPIView):
    """
    get:
        Returns the profile of user.

    put:

        parameters: [first_name, last_name, gender]
    """

    # queryset = get_user_model().objects.select_related(
    #     'country', 'state').prefetch_related(
    #         Prefetch('hobbies', queryset=Hobby.objects.filter(is_active=True)))
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user


@extend_schema(tags=['api.v1 user-info'])
class DeleteAccount(APIView):
    """
    delete:
        Delete an existing User instance.
    """

    permission_classes = [IsAuthenticated,]

    def delete(self, request):
        user = request.user  # get_user_model().objects.get(pk=request.user.pk)
        if not request.user.two_step_password:
            user.delete()
            return Response(
                {"message": _("Your account has been successfully deleted.")},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            serializer = PasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            password = serializer.data.get("password")
            check_password: bool = user.check_password(password)

            if check_password:
                user.delete()

                return Response(
                    {"message": _("Your account has been successfully deleted.")},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"message": _("The password entered is incorrect.")},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
