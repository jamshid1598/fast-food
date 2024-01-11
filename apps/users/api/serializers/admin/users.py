from django.db import transaction

from django.forms import model_to_dict
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import User, BlockedEmail
from user.validators import calculate_age, validate_age


class UserSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('fcm_token', 'two_step_password', 'last_login', 'user_permissions', 'groups', '_age')
        extra_kwargs = {
            'password': {'write_only': True},
            'age': {'read_only': True},
        }

    def validate_password(self, password: str) -> str:
        return make_password(password)

    def validate(self, attrs):
        if 'birthdate' in attrs:
            validate_age(attrs['birthdate'])
            attrs['age'] = calculate_age(attrs['birthdate'])
        return attrs

    def get_likes(self, user):
        return user.likes

    def get_blocks(self, user):
        return user.blocks

    def get_absolute_uri(self, url):
        return self.context['request'].build_absolute_uri(url)

    def get_images(self, user):
        images = user.created_profileimages.only('id', 'media')
        return [{'id': media.id, 'image': self.get_absolute_uri(media.media.url)} for media in images]

    def get_main_image(self, user):
        media = user.main_image if user.main_image else user.created_profileimages.first()

        if media and media.media.name:
            return {
                "id": media.id,
                "image": self.context['request'].build_absolute_uri(media.media.url)
            }
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.country:
            data['country'] = model_to_dict(instance.country, fields=('id', 'name_uz', 'name_ru', 'name_en'))
        if instance.state:
            data['state'] = model_to_dict(instance.state, fields=('id', 'name_uz', 'name_ru', 'name_en'))

        data['hobbies'] = instance.hobbies.values('id', 'name_uz', 'name_ru', 'name_en')

        data['main_image'] = self.get_main_image(instance)
        data['age'] = instance.age
        data['likes'] = self.get_likes(instance)
        data['blocks'] = self.get_blocks(instance)

        if hasattr(instance, 'has_filters'):
            data['has_filters'] = instance.has_filters

        return data


class UserDetailFilter(serializers.Serializer):
    id = serializers.UUIDField()


class BlockedEmailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BlockedEmail
        fields = ('email', 'id', 'user')

        extra_kwargs = {
            'email': {'read_only': True},
            'user': {'write_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop('user')

        user.created_profileimages.all().delete()
        user.reactions.all().delete()
        user.created_reactions.all().delete()

        email = user.email
        user.delete()
        return super().create({'email': email})

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "email": instance.email
        }
