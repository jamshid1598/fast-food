from rest_framework import serializers

from fastfood.models import Restaurant
from users.models import Employee, UserType


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        obj = Restaurant.objects.create(**validated_data)
        Employee.objects.create(user=user, restaurant=obj, user_type=UserType.ADMIN)
        return obj


class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']
