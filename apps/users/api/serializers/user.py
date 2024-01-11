from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from user.models import User, ProfileImage
from user.validators import calculate_age

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from core.api.serializers.country import CountryReadSerializer, StateSerializer
from .profile import UserImageSerializer


class AuthenticationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)


class LoginSerializer(AuthenticationSerializer):
    password = serializers.CharField(max_length=100)


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        try:
            int(value)
        except ValueError as e:
            print("Invalid code: ", e)
            raise serializers.ValidationError("Invalid Code.")

        return value

    # @property
    # def errors(self):
    #     errors = super().errors()
    #     errors = dict(errors)
    #     if 'code' in errors:
    #         errors['error_code'] = errors['code'][0].code

    #     return errors


class PasswordSerializer(serializers.Serializer):
    """
        Base serializer two-step-password.
    """
    password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                {"Error": "Your passwords didn't match."}
            )

        return data


class ResetPasswordSerializer(AuthenticationSerializer, OtpSerializer, PasswordSerializer):
    pass


class ChangePasswordSerializer(PasswordSerializer):
    old_password = serializers.CharField(max_length=20)


class RefreshTokenSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class UsersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id", "username", "phone", "email",
            "first_name", "last_name", "gender",
        ]
        extra_kwargs = {
            # 'passport': {
            #     'required': False,
            #     'allow_null': True,
            # }
        }


class UserDetailUpdateDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password",)
        read_only_fields = ('last_login',)
        extra_kwargs = {
            # 'passport': {
            #     'required': False,
            #     'allow_null': True,
            # }
        }


class UserFcmTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=600)


class UserProfileSerializer(serializers.ModelSerializer):

    age = serializers.SerializerMethodField(method_name='get_age')
    images = serializers.SerializerMethodField()
    canUploadMedia = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "phone", "email",
            "first_name", "last_name", "gender",
            "two_step_password",
            "country", "state", "hobbies", "birthdate", "age", "bio",
            "images", "main_image",
            'canUploadMedia',
        ]
        read_only_fields = ('id', 'two_step_password', 'age')

    def get_age(self, user):
        return user.age

    def get_images(self, user):
        return UserImageSerializer(
            user.created_profileimages.all(), many=True, context=self._context
        ).data

    def validate_main_image(self, image):
        if image.created_by != self.context['request'].user:
            raise serializers.ValidationError({
                'error_code': "image_not_yours",
            })

        return image

    def get_canUploadMedia(self, user):
        return user.can_upload_media()

    def to_representation(self, instance):
        data = super(UserProfileSerializer, self).to_representation(instance)

        data['country'] = CountryReadSerializer(instance.country).data if instance.country else None
        data['state'] = StateSerializer(instance.state).data if instance.state else None
        data['hobbies'] = instance.hobbies.values('id', 'name_en', 'name_ru', 'name_uz')

        main_image = instance.main_image
        if not main_image:
            main_image = instance.created_profileimages.first()

        if main_image:
            data['main_image'] = UserImageSerializer(main_image, context=self.context).data

        return data

    def validate(self, attrs):

        if 'birthdate' in attrs:
            _age = calculate_age(attrs['birthdate'])
            if _age < 19:
                raise serializers.ValidationError(
                    {
                        "error_code": "age_limit_error",
                        "message": "User must be older than 19 years old.",
                    }
                )
            attrs['_age'] = _age

        return attrs
