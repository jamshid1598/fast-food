from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.api.serializers.profile import UserImageSerializer, ProfileImageSerializer
from user.models import ProfileImage


class ProfileImageQuerysetMixin:
    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class ProfileImageAPI(ProfileImageQuerysetMixin, ListCreateAPIView):
    serializer_class = UserImageSerializer
    queryset = ProfileImage.objects.all().select_related('created_by')
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @swagger_auto_schema(
        tags=['api.v1 user'],
        responses={200: UserImageSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['api.v1 user'],
        # request_body=CountryWriteSerializer,
        responses={201: UserImageSerializer()},
    )
    def post(self, request, *args, **kwargs):
        if not request.user.can_upload_media():
            return Response({
                "error_code": "mediaUploadLimitReached",
            }, status=403)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user
        )

        if not self.request.user.main_image:
            self.request.user.main_image = serializer.instance
            self.request.user.save(update_fields=('main_image',))


class ProfileImageDetailAPI(ProfileImageQuerysetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = UserImageSerializer
    queryset = ProfileImage.objects.all().select_related('created_by')
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user
        )

    @swagger_auto_schema(
        tags=['api.v1 user'],
        responses={200: UserImageSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['api.v1 user'],
        responses={200: UserImageSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['api.v1 user'],
        responses={200: UserImageSerializer()},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['api.v1 user'],
        responses={204: {}},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProfileMainImageAPI(APIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['api.v1 user'],
        responses={200: ProfileImageSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_id = serializer.validated_data.get('image')
        try:
            image = ProfileImage.objects.get(id=image_id, created_by=request.user)
            request.user.main_image = image
            request.user.save(update_fields=['main_image'])
            return Response({"status": "ok"})
        except ProfileImage.DoesNotExist:
            return Response({
                "error_code": "imageNotFound"
            }, status=404)
