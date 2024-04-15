import pytest

from ninja_extra.testing import TestClient
import json

from src.main.utils import make_request
from src.users.api import CustomTokenObtainPairController
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings


obtain_token_client = TestClient(CustomTokenObtainPairController)
headers = {
    'Accept-Language': 'en'
}

schema = SchemaControl(api_settings)
obtain_pair_schema = schema.obtain_pair_schema.get_response_schema()


@pytest.fixture(scope="session")
def access_token():
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
    token = response.json()['access']
    return f'Bearer {token}'