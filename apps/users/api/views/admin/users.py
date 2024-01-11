from django.db.models import Count, Q, F, Value, Case, When

from drf_yasg.utils import swagger_auto_schema

from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAdminUser

from core.models import REACTION

from user.models import User, BlockedEmail, ProfileImage
from user.api.filters.admin.users import UserFilter
from user.api.serializers.admin.users import UserSerializer, BlockedEmailSerializer
from user.api.serializers.admin.profile_image import SetUserMainImageSerializer, ImageSerializer
from user.api.pagination import UsersPaginationForAdmin, BlockedEmailPagination


class UserAPI(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filterset_class = UserFilter
    pagination_class = UsersPaginationForAdmin

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by('-created_at').select_related('country', 'state', 'main_image').prefetch_related(
            'hobbies', 'created_profileimages'
        ).annotate(
            likes=Count(F('reactions'), filter=Q(reactions__reaction=REACTION.LIKED)),
            blocks=Count(F('reactions'), filter=Q(reactions__reaction=REACTION.BLOCKED)),
            has_filters=Case(
                When(Q(filter_options__isnull=False), then=Value(True)), default=Value(False)),
        )

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',)
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',)
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        super().get_object()
        queryset = self.filter_queryset(self.get_queryset())

        user = queryset.filter(**{self.lookup_field: self.kwargs[self.lookup_field]}).select_related(
            'country', 'state', 'main_image').prefetch_related(
            'hobbies', 'created_profileimages').annotate(
                likes=Count(F('reactions'), filter=Q(reactions__reaction=REACTION.LIKED)),
                blocks=Count(F('reactions'), filter=Q(reactions__reaction=REACTION.BLOCKED)),
                has_filters=Case(
                    When(Q(filter_options__isnull=False), then=Value(True)), default=Value(False)
                ),
            ).first()
        if user:
            return user
        raise NotFound("userNotFound", 404)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',)
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',)
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',)
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',)
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BlockUserAPI(ListCreateAPIView):
    queryset = BlockedEmail.objects.all()
    serializer_class = BlockedEmailSerializer
    pagination_class = BlockedEmailPagination
    permission_classes = [IsAdminUser]
    filterset_fields = {
        'email': ['istartswith'],
    }

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BlockUserDetailAPI(RetrieveDestroyAPIView):
    """Not a blocked user, only blocked email.
        so `not use UUID`, use only `Integer ID`"""

    queryset = BlockedEmail.objects.all()
    serializer_class = BlockedEmailSerializer
    pagination_class = BlockedEmailPagination
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = queryset.filter(**{self.lookup_field: self.kwargs[self.lookup_field]}).first()
        if obj:
            return obj
        raise NotFound('objNotFound')

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserProfileMainImageAPI(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SetUserMainImageSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
        responses={200: SetUserMainImageSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
        responses={200: SetUserMainImageSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = queryset.filter(**{self.lookup_field: self.kwargs[self.lookup_field]}).first()
        if obj:
            return obj
        raise NotFound('objNotFound')


class ProfileImageCreateAPI(CreateAPIView):
    queryset = ProfileImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProfileImageDeleteAPI(DestroyAPIView):
    queryset = ProfileImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = queryset.filter(**{self.lookup_field: self.kwargs[self.lookup_field]}).first()
        if obj:
            return obj
        raise NotFound('objNotFound')
