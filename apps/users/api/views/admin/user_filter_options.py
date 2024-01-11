from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound

from user.models import User
from user.api.serializers.admin.user_filter_options import UserFilterOptionsSerializer
from user.api.exceptions import NoException


class UserFilterOptionsAPI(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserFilterOptionsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = queryset.filter(**{self.lookup_field: self.kwargs[self.lookup_field]}).first()
        try:
            return obj.filter_options
        except AttributeError:
            raise NotFound('objNotFound')
        except Exception:
            raise NoException("userNotSetYet")

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=('api.v1 admin-actions users',),
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
