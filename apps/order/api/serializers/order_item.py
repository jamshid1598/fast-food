from rest_framework import serializers

from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'fastfood', 'name', 'count', 'price']


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['fastfood', 'name', 'count', 'price']
