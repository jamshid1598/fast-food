from rest_framework import serializers
from rest_framework.exceptions import NotFound

from user.models import ProfileImage, User


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ProfileImage
        fields = ('media', 'user')
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def validate(self, attrs):
        attrs['created_by'] = attrs.pop('user')
        return attrs

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "media": self.context['request'].build_absolute_uri(instance.media.url)
        }


class SetUserMainImageSerializer(serializers.ModelSerializer):
    image = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('image',)

    def validate(self, attrs):
        image = ProfileImage.objects.filter(
            created_by=self.instance, id=attrs.pop('image')
        ).first()

        if image is None:
            raise NotFound('imageNotFound')
        attrs['main_image'] = image
        return attrs

    def to_representation(self, instance):
        return {"detail": "mainImageSetSuccessfully"}


class IDSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
