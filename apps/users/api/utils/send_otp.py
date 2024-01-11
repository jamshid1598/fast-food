from django.core.cache import cache
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from user.api.utils.eskiz import SendOTP
from user.api.utils.email import SendEmailOTP
from config.extensions.utils import otp_generator, get_client_ip


def send_otp(request, phone_email):
    with_email = SendEmailOTP()
    with_sms = SendOTP()
    otp = otp_generator()
    ip = get_client_ip(request)

    cache.set(f"{ip}-for-authentication", phone_email, settings.EXPIRY_TIME_OTP)
    cache.set(phone_email, otp, settings.EXPIRY_TIME_OTP)

    if phone_email.isdigit():
        response = with_sms.send_otp(phone_email, otp)
    else:
        response = with_email.send_otp(phone_email, otp)

    return response
