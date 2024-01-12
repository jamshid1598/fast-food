from rest_framework import serializers

from order.models import Order, OrderItem
from order.api.serializers.order_item import (
    OrderItemSerializer, CreateOrderItemSerializer,
)
from order.utils import get_delivery_time


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        obj = Order.objects.create(**validated_data, user=user)
        return obj

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['item_count'] = instance.orderitems.count()
        return data


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['order_items'] = OrderItemSerializer(instance.orderitems.all(), many=True).data
        return data


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = serializers.ListField(child=CreateOrderItemSerializer(), max_length=100, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        exclude = ['status', "user", "delivery_time"]

    def create(self, validated_data):
        user = self.context['request'].user
        order_items = validated_data.pop('order_items', None)
        instance = Order.objects.create(**validated_data, user=user)

        if order_items:
            for item in order_items:
                order_items = OrderItem.objects.create(**item, order=instance)

        instance.delivery_time = get_delivery_time(instance)
        instance.save(update_fields=['delivery_time'])
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['order_items'] = OrderItemSerializer(instance.orderitems.all(), many=True).data
        data['delivery_time'] = instance.delivery_time
        return data


class OrderUpdateSerializer(serializers.ModelSerializer):
    order_items = serializers.ListField(child=CreateOrderItemSerializer(), max_length=100, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        exclude = ["user", "delivery_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['order_items'] = OrderItemSerializer(instance.orderitems.all(), many=True).data
        data['delivery_time'] = instance.delivery_time
        return data

    def update(self, instance, validated_data):
        order_items = validated_data.pop('order_items', None)
        instance.restaurant = validated_data.get('restaurant') or instance.restaurant
        instance.total_price = validated_data.get('total_price') or instance.total_price
        instance.status = validated_data.get('status') or instance.status
        instance.lon = validated_data.get('lon') or instance.lon
        instance.lat = validated_data.get('lat') or instance.lat
        instance.address = validated_data.get('address') or instance.address
        instance.delivery_time = get_delivery_time(instance)
        instance.save()

        if order_items:
            order_item_ids = list(OrderItem.objects.filter(order=instance).values_list('id', flat=True))
            for item in order_items:
                if item.get('id'):
                    order_item_ids.remove(item.get('id'))
                    OrderItem.objects.filter(id=item.get('id')).update(**item)
                else:
                    OrderItem.objects.create(**item, order=instance)

            OrderItem.objects.filter(id__in=order_item_ids).delete()

        instance.delivery_time = get_delivery_time(instance)
        instance.save()

        return super(OrderUpdateSerializer, self).update(instance, validated_data)
