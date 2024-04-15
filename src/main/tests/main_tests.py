import pytest
from ninja_extra.testing import TestClient
from jsonschema import validate
from src.main.api import MainController
import jsonschema
from src.main.schemas import NewsSchema, NewsSectionSchema, SettingsOutSchema, ReviewsSectionSchema, WhyChooseUsSchema, \
    InstaSchema
from src.main.utils import make_request

client = TestClient(MainController)
headers = {
    'Accept-Language': 'uk'
}


@pytest.mark.django_db
class TestMainController:
    def test_get_instagram(self):
        request_str = f'/instagram/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=InstaSchema,
                                          client=client,
                                          headers=headers)

        assert is_valid is True
        assert response.status_code == 200

    def test_get_settings(self):
        request_str = f'/settings/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=SettingsOutSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is True
        assert response.status_code == 200

    def test_get_why_choose_us(self):
        request_str = f'/why-choose-us/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=WhyChooseUsSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is is_valid
        assert response.status_code == 200

    @pytest.mark.parametrize("payload,expected_status,schema_status",
                             [
                                 (
                                         '?page=1&page_size=4',
                                         200,
                                         True,

                                 ),
                                 (
                                         '?page=1',
                                         422,
                                         False,
                                 ),
                                 (
                                         '?page_size=1',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_get_reviews(self, payload, expected_status, schema_status):
        request_str = f'/reviews/{payload}'
        response, is_valid = make_request(request_str=request_str,
                                          schema=ReviewsSectionSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is schema_status
        assert response.status_code == expected_status

    @pytest.mark.parametrize("payload,expected_status,schema_status",
                             [
                                 (
                                         '?page=1&page_size=4',
                                         200,
                                         True,

                                 ),
                                 (
                                         '?page=1',
                                         422,
                                         False,
                                 ),
                                 (
                                         '?page_size=1',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_get_news(self, payload, expected_status, schema_status):
        request_str = f'/news/{payload}'
        response, is_valid = make_request(request_str=request_str,
                                          schema=NewsSectionSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is schema_status
        assert response.status_code == expected_status
