from rest_framework import serializers

from order.models import Order, OrderItem
from order.api.serializers.order_item import (
    OrderItemSerializer, CreateOrderItemSerializer,
)
from fastfood.api.serializers.fastfood import FastFoodOrderSerializer


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
        data['oreder_items'] = OrderItemSerializer(instance.orderitems.all(), many=True).data
        return data


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = serializers.ListField(child=CreateOrderItemSerializer(), max_length=100, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        exclude = ['is_completed', 'is_confirmed', "user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['oreder_items'] = OrderItemSerializer(instance.orderitems.all(), many=True).data
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        order_items = validated_data.pop('order_items')
        instance = Order.objects.create(**validated_data, user=user)
        if order_items:
            order_items = OrderItem.objects.create(**order_items, order=instance)
        return instance


class OrderUpdateSerializer(serializers.ModelSerializer):
    order_items = serializers.ListField(child=CreateOrderItemSerializer(), max_length=100, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        exclude = ["user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['oreder_items'] = OrderItemSerializer(instance.orderitems.all(), many=True).data
        return data

    def update(self, instance, validated_data):
        order_items = validated_data.pop('order_items')
        instance.restaurant = validated_data.get('restaurant') or instance.restaurant
        instance.total_price = validated_data.get('total_price') or instance.total_price
        instance.is_confirmed = validated_data.get('is_confirmed') or instance.is_confirmed
        instance.is_completed = validated_data.get('is_completed') or instance.is_completed
        instance.lon = validated_data.get('lon') or instance.lon
        instance.lat = validated_data.get('lat') or instance.lat
        instance.address = validated_data.get('address') or instance.address
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

        return super(OrderUpdateSerializer, self).update(instance, validated_data)
