from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from drf_spectacular.utils import extend_schema


from users.permissions import IsAdmin
from fastfood.models import Restaurant
from fastfood.api.serializers.restaurant import RestaurantSerializer


class RestaurantList(ListAPIView):
    """
    get:
        Returns a list of all Restaurant.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny,]
    filterset_fields = ["name", 'address',]
    search_fields = ["name", "address", "description"]
    ordering_fields = ("id", "name", "address")

    def get_queryset(self):
        return Restaurant.objects.values(
            "id", "name", "description", "lon", "lat", "address"
        )

    @extend_schema(tags=['api.v1 Restaurant'], request=RestaurantSerializer, responses={200: RestaurantSerializer})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RestaurantCreate(CreateAPIView):
    """
    post:
        Returns a newly created Restaurant instance.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated,]

    @extend_schema(tags=['api.v1 Restaurant'], request=RestaurantSerializer, responses={201: RestaurantSerializer})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RestaurantDetail(RetrieveAPIView):
    """
    get:
        Returns the detail of a restaurant instance.

        parameters: [pk]
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny,]

    @extend_schema(tags=['api.v1 Restaurant'], request=RestaurantSerializer, responses={200: RestaurantSerializer})
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RestaurantUpdate(UpdateAPIView):
    """
    put:
        Update the detail of a restaurant instance

        parameters: [pk]
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdmin,]

    @extend_schema(tags=['api.v1 Restaurant'], request=RestaurantSerializer, responses={202: RestaurantSerializer})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(tags=['api.v1 Restaurant'], request=RestaurantSerializer, responses={202: RestaurantSerializer})
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RestaurantDelete(DestroyAPIView):
    """
    delete:
        Delete a restaurant instance.
        
        parameters: [pk]
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdmin,]

    @extend_schema(tags=['api.v1 Restaurant'], request=RestaurantSerializer, responses={204: RestaurantSerializer})
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
