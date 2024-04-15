import json
import pytest
from django.test import TestCase
from ninja.testing.client import NinjaResponse
from ninja_extra.testing import TestClient
from ninja_jwt.schema_control import SchemaControl
from src.main.utils import make_request
from src.users.api import CustomTokenObtainPairController, AuthController
from ninja_jwt.settings import api_settings
from loguru import logger

from src.users.schemas import MessageOutSchema

obtain_token_client = TestClient(CustomTokenObtainPairController)
client = TestClient(AuthController)
headers = {
    'Accept-Language': 'en'
}

schema = SchemaControl(api_settings)
obtain_pair_schema = schema.obtain_pair_schema.get_response_schema()
refresh_schema = schema.obtain_pair_refresh_schema.get_response_schema()


@pytest.mark.django_db
class TestAuthController:

    def test_obtain_token(self):
        auth = {
            "password": "sword123",
            "email": "user@example.com",
        }
        payload = json.dumps(auth)
        response, is_valid = make_request(request_str=f'/pair',
                                          schema=obtain_pair_schema,
                                          client=obtain_token_client,
                                          method='post',
                                          payload=payload,
                                          headers=headers)
        assert response.status_code == 200
        assert is_valid is True

    @pytest.mark.parametrize("payload,expected_status,schema_status",
                             [
                                 (
                                         {
                                             "email": "test1@example.com",
                                             "password": "string",
                                             "notify_me": True
                                         },
                                         200,
                                         True,
                                 ),
                                 (
                                         {
                                             "email": "test1@example.com",
                                             "password": "string",
                                             "notify_me": True
                                         },
                                         409,
                                         False,
                                 ),
                                 (
                                         {
                                             "email": "error",
                                             "password": "string",
                                             "notify_me": True

                                         },
                                         422,
                                         False,
                                 ),
                                 (
                                         {
                                             "email": "error@example.com",
                                             "password": "string"
                                         },
                                         422,
                                         False,
                                 ),
                                 (
                                         {
                                             "password": "string",
                                         },
                                         422,
                                         False,
                                 ),
                                 (
                                         {
                                             "notify_me": True
                                         },
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_registration(self, payload, expected_status, schema_status):
        payload = json.dumps(payload)
        response, is_valid = make_request(request_str=f'/registration/',
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='post',
                                          payload=payload,
                                          headers=headers)
        if expected_status == 409:
            response, is_valid = make_request(request_str=f'/registration/',
                                              schema=MessageOutSchema,
                                              client=client,
                                              method='post',
                                              payload=payload,
                                              headers=headers)
        assert response.status_code == expected_status
        assert is_valid is schema_status
