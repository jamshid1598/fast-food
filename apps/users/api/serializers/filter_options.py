from rest_framework import serializers

from user.models import FilterOptions


class FilterOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterOptions
        exclude = ('created_by', 'updated_by')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['countries'] = instance.countries.values('id', 'name_uz', 'name_en', 'name_ru')
        data['hobbies'] = instance.hobbies.values('id', 'name_uz', 'name_en', 'name_ru')
        return data
