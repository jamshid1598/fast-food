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


from users.permissions import IsAdmin, IsAdminOrWaiter
from order.models import Order
from order.api.serializers.order import (
    OrderSerializer, OrderDetailSerializer,
    OrderCreateSerializer,
)


class ClientOrderList(ListAPIView):
    """
    get:
        Returns a list of all Client Orders.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,]
    filterset_fields = ["restaurant", 'user', 'is_confirmed', 'is_completed']
    search_fields = ["restaurant", 'user']
    ordering_fields = ('id', 'user', 'is_confirmed', 'is_completed')

    @extend_schema(
        tags=['api.v1 Client-Orders'],
        request=OrderSerializer,
        responses={200: OrderSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ClientOrderDetail(RetrieveAPIView):
    """
    get:
        Returns the detail of a order instance.

        parameters: [pk]
    """

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated,]

    @extend_schema(
        tags=['api.v1 Client-Orders'],
        request=OrderDetailSerializer,
        responses={200: OrderDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ClientOrderCreate(CreateAPIView):
    """
    post:
        Create new order.
    """

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated,]

    @extend_schema(
        tags=['api.v1 Client-Orders'],
        request=OrderCreateSerializer,
        responses={201: OrderCreateSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
