from rest_framework import serializers

from user.models import FilterOptions
from core.api.serializers.country import CountryReadSerializer
from core.api.serializers.hobby import HobbySerializer


class UserFilterOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterOptions
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['hobbies'] = HobbySerializer(instance.hobbies.all(), many=True).data
        data['countries'] = CountryReadSerializer(instance.countries.all(), many=True).data

        return data
