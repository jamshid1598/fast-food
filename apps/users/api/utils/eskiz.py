import requests
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from user.models import SMSToken, OTPStatus
# from bot.views.bot_errorhandler import send_message_to_admin


def response_json(response):
    data = {}
    try:
        data = response.json()
    except Exception as e:
        print("Error on converting response to json: ", e)
        message = "Error on converting response to json: %s" % e
        print(message)
        # send_message_to_admin(message)
        data['message'] = e

    return data


class SendOTP:
    AUTH_URL = "https://notify.eskiz.uz/api/auth/login"
    SEND_OTP = "https://notify.eskiz.uz/api/message/sms/send"
    CALLBACK_URL = "https://%s%s" % (settings.SERVER_DOMAIN, '/users/api/opt-status/')

    def __init__(self):
        self.token = None

    def check_token(self):
        obj = SMSToken.objects.last()

        if obj:
            now = timezone.now()
            timedelta = now - obj.created_at
            if timedelta.days < 29:
                self.token = obj.token
                return True

            obj.is_valid = False
            obj.save()

        return False

    def get_token(self):

        payload = {
            'email': settings.ESKIZ_EMAIL,
            'password': settings.ESKIZ_PASSWORD
        }

        try:
            response = requests.request("POST", self.AUTH_URL, headers={}, data=payload, files=[])
        except Exception as e:
            print("Error on sending request to get new token: ", e)
            message = "<b>Error on sending request to get new token:</b> \n\n<i>%s</i>" % e
            print(message)
            # send_message_to_admin(message)

        if hasattr(response, 'status_code'):
            response_js = response_json(response)

            if response.status_code in [200, 201]:
                data = response_js.get('data', {})
                token = data.get('token', None)
                if token is not None:
                    SMSToken.objects.create(token=token)
                else:
                    message = "<b>'token' not found in response.</b> " \
                             " \n\nstatus code: %s \nresponse: %s" % (response.status_code, response_js)
                    print(message)
                    # send_message_to_admin(message)

            else:
                message = "<b>Error on getting new token in get_token() method:</b> \n\nresponse: %s" % response_js
                print(message)
                # send_message_to_admin(message)

        return token

    def sms_response(self, response, code=None):
        context = {'otp': code}

        if hasattr(response, 'status_code'):
            status_code = response.status_code
            response_js = response_json(response)
            message = response_js.get('message')
            context['message'] = message
            return Response(context, status=status_code)

        return Response({"message": _("bad request, please contact support center.")}, status=status.HTTP_400_BAD_REQUEST)

    def send_otp(self, phone, code):
        response = None

        if not self.check_token():
            self.token = self.get_token()

        if self.token:
            bearer_token = 'Bearer %s' % self.token
            headers = {'Authorization': bearer_token}

            payload = {
                'mobile_phone': str(phone)[1:],
                'message': 'YaTaxi sms xizmati.\nUshbu kodni hech kimga bermang!\nKod: %s' % code,
                'from': '4546',
                'callback_url': self.CALLBACK_URL
            }

            try:
                response = requests.request("POST", self.SEND_OTP, headers=headers, data=payload, files=[])
            except Exception as e:
                print("Error in sending sms otp: %s" % e)
                message = "<b>Error in sending sms otp:</b> \n\n<i>%s</i>" % e
                print(message)
                # send_message_to_admin(message)

            response_js = response_json(response)

            OTPStatus.objects.create(
                phone=phone,
                user_sms_id=response_js.get('id'),
                status=response_js.get('status'),
                message=response_js.get('message')
            )
            # send_message_to_admin("message: %s" % response_js)

        return self.sms_response(response, code)
