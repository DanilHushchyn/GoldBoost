from django.http import HttpRequest
from django.middleware.locale import LocaleMiddleware
from ninja import Header

from config import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used

from django.utils import translation

from src.main.utils import LangEnum


class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest()):
        print(request.path_info)
        # print(111)
        # print(request.META['HTTP_ACCEPT_LANGUAGE'])
        print(request.headers['Accept-Language'])
        response = self.get_response(request,)

        return response
