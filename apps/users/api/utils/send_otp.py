from django.core.cache import cache
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from users.api.utils.eskiz import SendOTP
from config.extensions.utils import otp_generator, get_client_ip


def send_otp(request, phone):
    otp = otp_generator()
    ip = get_client_ip(request)
    cache.set(f"{ip}-for-authentication", phone, settings.EXPIRY_TIME_OTP)
    cache.set(phone, otp, settings.EXPIRY_TIME_OTP)

    if settings.DEBUG:
        context = {"otp": f"{otp}"}
        return Response(context, status=status.HTTP_200_OK,)

    obj = SendOTP()
    response = obj.send_otp(phone, otp)

    return response
