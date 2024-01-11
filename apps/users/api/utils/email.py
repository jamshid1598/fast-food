from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class SendEmailOTP:

    def send_otp(self, phone_email, otp):
        subject = "Confirmation code for tinder.uz"
        html_message = render_to_string(
            'email/confirmation_email.html', {
                'message': "Confirmation code for tinder.uz",
                'email': phone_email,
                'otp': otp,
            }
        )
        message = strip_tags(html_message)
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[phone_email, 'dovurovjamshid982@gmail.com'],
                html_message=html_message,
            )
            response = Response({'message': 'otp code send successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': 'error on sending otp code: %s' % e}, status=status.HTTP_400_BAD_REQUEST)

        return response
