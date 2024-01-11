from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from user.models import FilterOptions
from user.api.serializers.filter_options import FilterOptionsSerializer


class SetFilterOptionsAPI(RetrieveUpdateAPIView):
    serializer_class = FilterOptionsSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return FilterOptions.objects.prefetch_related('countries', 'hobbies')

    def get_object(self):
        obj, _ = self.get_queryset().get_or_create(created_by=self.request.user)
        return obj

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=('api.v1 filter-users', ))
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
