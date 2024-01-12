from django.utils.translation import gettext_lazy as _
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from drf_spectacular.utils import extend_schema


from users.permissions import IsAdminOrWaiter
from order.models import Order, OrderItem
from order.api.serializers.order_item import OrderItemSerializer


class OrderItemList(ListAPIView):
    """
    get:
        Returns a list of all Order Items.
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrWaiter,]
    filterset_fields = ['order', 'fastfood', 'name', 'count', 'price']
    search_fields = ["order", 'fastfood', 'name']
    ordering_fields = ("order", 'fastfood')

    @extend_schema(
        tags=['api.v1 Order Items'],
        request=OrderItemSerializer,
        responses={200: OrderItemSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderItemDetail(RetrieveAPIView):
    """
    get:
        Returns the detail of a order-item instance.

        parameters: [pk]
    """

    queryset = Order.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(
        tags=['api.v1 Order Items'],
        request=OrderItemSerializer,
        responses={200: OrderItemSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderItemUpdate(UpdateAPIView):
    """
    put:
        Update the detail of a order-item instance

        parameters: [pk]
    """

    queryset = Order.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(
        tags=['api.v1 Order Items'],
        request=OrderItemSerializer,
        responses={202: OrderItemSerializer}
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['api.v1 Order Items'],
        request=OrderItemSerializer,
        responses={202: OrderItemSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderItemDelete(DestroyAPIView):
    """
    delete:
        Delete a order instance.
        
        parameters: [pk]
    """

    queryset = Order.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(
        tags=['api.v1 Order Items'],
        request=OrderItemSerializer,
        responses={202: OrderItemSerializer}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
