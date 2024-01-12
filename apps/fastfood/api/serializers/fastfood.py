from rest_framework import serializers

from fastfood.models import FastFood
from fastfood.api.serializers.restaurant import RestaurantInfoSerializer


class FastFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastFood
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['restaurant'] = RestaurantInfoSerializer(instance.restaurant).data
        return data


class FastFoodCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastFood
        exclude = ['restaurant']

    def create(self, validated_data):
        user = self.context['request'].user
        restaurant = user.employee.restaurant
        obj = FastFood.objects.create(restaurant=restaurant, **validated_data)
        return  obj

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['restaurant'] = RestaurantInfoSerializer(instance.restaurant).data
        return data


class FastFoodOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastFood
        fields = ['id', 'name']
