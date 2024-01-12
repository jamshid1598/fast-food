from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from drf_spectacular.utils import extend_schema


from users.permissions import IsAdmin, IsAdminOrWaiter
from fastfood.api.serializers.fastfood import (
    FastFoodSerializer, FastFoodCreateUpdateSerializer
)
from fastfood.models import FastFood


class FastFoodList(ListAPIView):
    """
    get:
        Returns a list of fast-food list.
    """

    queryset = FastFood.objects.all()
    serializer_class = FastFoodSerializer
    permission_classes = [AllowAny,]
    filterset_fields = ["restaurant", 'name',]
    search_fields = ["restaurant", "name",]
    ordering_fields = ("id", "name", "price")

    @extend_schema(tags=['api.v1 fastfood'], request=FastFoodSerializer, responses={200: FastFoodSerializer})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FastFoodCreate(CreateAPIView):
    """
    post:
        Created new fast-food.
    """

    queryset = FastFood.objects.all()
    serializer_class = FastFoodCreateUpdateSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(
        tags=['api.v1 fastfood'],
        request=FastFoodCreateUpdateSerializer,
        responses={201: FastFoodCreateUpdateSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FastFoodDetail(RetrieveAPIView):
    """
    get:
        Returns the detail of a fastfood instance.

        parameters: [pk]
    """

    queryset = FastFood.objects.all()
    serializer_class = FastFoodSerializer
    permission_classes = [AllowAny,]

    @extend_schema(tags=['api.v1 fastfood'], request=FastFoodSerializer, responses={200: FastFoodSerializer})
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class FastFoodUpdate(UpdateAPIView):
    """
    put:
        Update the detail of a restaurant instance

        parameters: [pk]
    """

    queryset = FastFood.objects.all()
    serializer_class = FastFoodCreateUpdateSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(
        tags=['api.v1 fastfood'],
        request=FastFoodCreateUpdateSerializer,
        responses={201: FastFoodCreateUpdateSerializer}
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['api.v1 fastfood'],
        request=FastFoodCreateUpdateSerializer,
        responses={201: FastFoodCreateUpdateSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FastFoodDelete(DestroyAPIView):
    """
    delete:
        Delete a fast-food instance.
        
        parameters: [pk]
    """

    queryset = FastFood.objects.all()
    serializer_class = FastFoodSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(tags=['api.v1 fastfood'], request=FastFoodSerializer, responses={200: FastFoodSerializer})
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
