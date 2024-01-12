from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from users.api.serializers.otp_status import OTPStatusSerializer


@extend_schema(tags=['api.v1 users'])
class OTPStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({}, status=status.HTTP_200_OK)
