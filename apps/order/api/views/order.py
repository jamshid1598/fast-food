from django.utils.translation import gettext_lazy as _
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from drf_spectacular.utils import extend_schema


from users.permissions import IsAdmin, IsAdminOrWaiter
from order.models import Order
from order.api.serializers.order import (
    OrderSerializer, OrderDetailSerializer,
    OrderUpdateSerializer,
)


class OrderList(ListAPIView):
    """
    get:
        Returns a list of all Orders.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrWaiter,]
    filterset_fields = ["restaurant", 'user', 'is_confirmed', 'is_completed']
    search_fields = ["restaurant", 'user']
    ordering_fields = ('id', 'user', 'is_confirmed', 'is_completed')

    @extend_schema(
        tags=['api.v1 Order'],
        request=OrderSerializer,
        responses={200: OrderSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderDetail(RetrieveAPIView):
    """
    get:
        Returns the detail of a order instance.

        parameters: [pk]
    """

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(
        tags=['api.v1 Order'],
        request=OrderDetailSerializer,
        responses={200: OrderDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderUpdate(UpdateAPIView):
    """
    put:
        Update the detail of a order instance

        parameters: [pk]
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrWaiter,]

    @extend_schema(tags=['api.v1 Order'], request=OrderUpdateSerializer, responses={202: OrderUpdateSerializer})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(tags=['api.v1 Order'], request=OrderUpdateSerializer, responses={202: OrderUpdateSerializer})
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderDelete(DestroyAPIView):
    """
    delete:
        Delete a order instance.
        
        parameters: [pk]
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin,]

    @extend_schema(tags=['api.v1 Order'], request=OrderSerializer, responses={204: OrderSerializer})
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
