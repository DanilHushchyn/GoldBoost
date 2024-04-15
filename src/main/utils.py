# -*- coding: utf-8 -*-
import json
from enum import Enum

from ninja.testing.client import NinjaResponse, TestClient
import pytest
from jsonschema import validate

import jsonschema
from loguru import logger
from ninja_extra import status
from ninja_extra.exceptions import APIException


class LangEnum(Enum):
    English = "en"
    Ukrainian = "uk"


class CustomAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Not Found"


@pytest.mark.django_db
def make_request(request_str: str, schema, client: TestClient,
                 headers: dict, method: str = 'get',
                 payload: str = None, ) \
        -> tuple[NinjaResponse, bool]:
    response = None
    match method:
        case 'post':
            response = client.post(request_str,
                                   headers=headers,
                                   data=payload)
        case 'get':
            response = client.get(request_str, headers=headers)
        case 'delete':
            response = client.delete(request_str, headers=headers)
        case 'patch':
            response = client.patch(request_str,
                                    headers=headers,
                                    data=payload)
    try:

        if isinstance(response.json(), list):
            for item in response.json():
                validate(instance=item,
                         schema=schema.json_schema())
        else:
            validate(instance=response.json(),
                     schema=schema.json_schema())

        is_valid = True
    except jsonschema.exceptions.ValidationError as e:
        is_valid = False
    return response, is_valid
