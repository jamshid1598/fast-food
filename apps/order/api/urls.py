from django.urls import path
from order.api.views.order import (
    OrderList, OrderDetail,
    OrderUpdate, OrderDelete
)
from order.api.views.client_order import (
    ClientOrderList, ClientOrderCreate, ClientOrderDetail,
)
from order.api.views.order_item import (
    OrderItemList, OrderItemDetail,
    OrderItemUpdate, OrderItemDelete
)


app_name = 'api'


urlpatterns = [
    path('order-list/', OrderList.as_view(), name='order-list'),
    path('order-detail/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('order-update/<int:pk>/', OrderUpdate.as_view(), name='order-update'),
    path('order-delete/<int:pk>/', OrderDelete.as_view(), name='order-delete'),

    # order items
    path('orderitem-list/', OrderItemList.as_view(), name='orderitem-list'),
    path('orderitem-detail/<int:pk>/', OrderItemDetail.as_view(), name='orderitem-detail'),
    path('orderitem-update/<int:pk>/', OrderItemUpdate.as_view(), name='orderitem-update'),
    path('orderitem-delete/<int:pk>/', OrderItemDelete.as_view(), name='orderitem-delete'),

    # client orders
    path('client-order-list/', ClientOrderList.as_view(), name='client-order-list'),
    path('client-order-create/', ClientOrderCreate.as_view(), name='client-order-create'),
    path('client-order-detail/<int:pk>/', ClientOrderDetail.as_view(), name='client-order-detail'),
]
