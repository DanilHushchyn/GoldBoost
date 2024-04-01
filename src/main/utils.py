from enum import Enum
from ninja_extra import status
from ninja_extra.exceptions import APIException


class LangEnum(Enum):
    English = "en"
    Ukrainian = "uk"


class CustomAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Not Found'
