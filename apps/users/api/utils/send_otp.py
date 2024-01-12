from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from string import digits
from secrets import choice as secret_choice
from users.api.utils.eskiz import SendOTP


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(secret_choice(char) for _ in range(size))


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
