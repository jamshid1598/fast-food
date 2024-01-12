import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from users.models import SMSToken, OTPStatus


def response_json(response):
	data = {}
	try:
		data = response.json()
	except Exception as e:
		print("Error on converting response to json: ", e)
		data['message'] = e

	return data


class SendOTP:
	AUTH_URL = "https://notify.eskiz.uz/api/auth/login"
	SEND_OTP = "https://notify.eskiz.uz/api/message/sms/send"
	CALLBACK_URL = "https://%s%s" % (settings.SERVER_DOMAIN, '/users/api/opt-status/')

	def get_new_token(self):

		token = ""
		payload = {
			'email': settings.ESKIZ_EMAIL,
			'password': settings.ESKIZ_PASSWORD
		}

		try:
			response = requests.request("POST", self.AUTH_URL, headers={}, data=payload, files=[])
		except Exception as e:
			print("Error on sending request to get new token: ", e)

		if hasattr(response, 'status_code'):
			response_js = response_json(response)
			if response.status_code in [200, 201]:
				data = response_js.get('data', {})
				token = data.get('token', None)
				if self.token is not None:
					SMSToken.objects.create(token=token)
					cache.set("eskiz_token", token, 2505600) # timeout=2505600 seconds = 29 days
				else:
					message = "'token' not found in response.\n\nstatus code: %s \nresponse: %s" % (response.status_code, response_js)
					print(message)
			else:
				message = "Error on getting new token in get_token() method:\n\nresponse: %s" % response_js
				print(message)

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
		token = cache.get('eskiz_token')
		if token is None:
			token = self.get_new_token()
		if token:
			bearer_token = 'Bearer %s' % token
			headers = {'Authorization': bearer_token}
			payload={
				'mobile_phone': str(phone)[1:],
				'message': 'Fast-food sms xizmati.\nUshbu kodni hech kimga bermang!\nKod: %s' % code,
				'from': '4546',
				'callback_url': self.CALLBACK_URL
			}

			try:
				response = requests.request("POST", self.SEND_OTP, headers=headers, data=payload, files=[])
			except Exception as e:
				message = "Error in sending sms otp:</b> \n\n%s" % e
				print(message)

			response_js = response_json(response)
			OTPStatus.objects.create(
				phone=phone,
				user_sms_id=response_js.get('id'),
				status=response_js.get('status'),
				message=response_js.get('message')
			)
		return self.sms_response(response, code)
