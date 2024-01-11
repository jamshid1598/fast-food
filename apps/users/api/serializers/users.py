from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from users.models import Users


class UsersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = [
            "id", "phone", "first_name", "last_name", "user_type",
        ]
        extra_kwargs = {
            'passport': {
                'required': False,
                'allow_null': True,
            }
        }


class UserDetailUpdateDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        exclude = ("password",)
        read_only_fields = ('last_login',)
        extra_kwargs = {
            'passport': {
                'required': False,
                'allow_null': True,
            }
        }


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = [
            "id", "phone", "first_name", "last_name",
            "user_type", "two_step_password",
        ]
        read_only_fields = ('id', 'phone', 'two_step_password')
        extra_kwargs = {
            'passport': {
                'required': False,
                'allow_null': True
            }
        }


class AuthenticationSerializer(serializers.Serializer):
    phone = PhoneNumberField(region='UZ')


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        try:
            int(value)
        except ValueError as _:
            raise serializers.ValidationError("Invalid Code.")

        return value


class GetTwoStepPasswordSerializer(serializers.Serializer):
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


class ChangeTwoStepPasswordSerializer(GetTwoStepPasswordSerializer):
    old_password = serializers.CharField(max_length=20)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        return data
