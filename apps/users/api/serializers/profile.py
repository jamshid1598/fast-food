
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


from user.models import ProfileImage, User


class UserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ('id', 'media')


class ProfileImageSerializer(serializers.Serializer):
    image = serializers.IntegerField()
