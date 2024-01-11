from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
