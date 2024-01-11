from django.shortcuts import get_object_or_404
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

from users.api.serializers.users import (
    UsersListSerializer,
    UserDetailUpdateDeleteSerializer,
    UserProfileSerializer,
    GetTwoStepPasswordSerializer,
)
from users.permissions import IsSuperUser


@extend_schema(tags=['api.v1 users'])
class UsersList(ListAPIView):
    """
    get:
        Returns a list of all existing users.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UsersListSerializer
    permission_classes = [IsSuperUser,]
    filterset_fields = ["user_type",]
    search_fields = ["phone", "first_name", "last_name",]
    ordering_fields = ("id", "user_type",)

    def get_queryset(self):
        return get_user_model().objects.values(
            "id", "phone",
            "first_name", "last_name",
            "user_type",
        )


@extend_schema(tags=['api.v1 users'])
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


@extend_schema(tags=['api.v1 users'])
class UserProfile(RetrieveUpdateAPIView):
    """
    get:
        Returns the profile of user.

    put:
        Update the detail of a user instance, `passport` is required if `user_type='driver'`.

        parameters: [first_name, last_name, gender, user_type, passport]
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user


@extend_schema(tags=['api.v1 users'])
class DeleteAccount(APIView):
    """
    delete:
        Delete an existing User instance.
    """

    permission_classes = [IsAuthenticated,]

    def delete(self, request):
        user = get_user_model().objects.get(pk=request.user.pk)
        if not request.user.two_step_password:
            user.delete()
            return Response(
                {"message": _("Your account has been successfully deleted.")},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            serializer = GetTwoStepPasswordSerializer(data=request.data)
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
