from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Bad request")
    default_code = 'bad_request'


class NoException(APIException):
    status_code = status.HTTP_200_OK
    default_detail = _("No Error occured.")
    default_code = 'no_exception'


class Forbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("Forbidden")
    default_code = 'forbidden'
