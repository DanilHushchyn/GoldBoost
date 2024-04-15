import pytest
from ninja_extra.testing import TestClient
from src.games.api import CatalogController
from src.main.utils import make_request
from src.games.schemas import *
from src.products.schemas import TabContentSchema

client = TestClient(CatalogController)
headers = {
    'Accept-Language': 'en'
}


@pytest.mark.django_db
class TestCatalogController:
    @pytest.mark.parametrize("page_id,expected_status,"
                             "schema_status",
                             [
                                 (
                                         1,
                                         200,
                                         True,
                                 ),
                                 (
                                         1000,
                                         404,
                                         False,
                                 ),
                                 (
                                         'abc',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_get_catalog_page(self, page_id, expected_status,
                              schema_status):
        response, is_valid = make_request(request_str=f'/{page_id}/',
                                          schema=CatalogPageSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is schema_status
        assert response.status_code == expected_status

    @pytest.mark.parametrize("page_id,expected_status,"
                             "schema_status",
                             [
                                 (
                                         1,
                                         200,
                                         True,
                                 ),
                                 (
                                         1000,
                                         404,
                                         False,
                                 ),
                                 (
                                         'abc',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_get_worth_look(self, page_id, expected_status,
                            schema_status):
        response, is_valid = make_request(request_str=f'/{page_id}/worth-look/',
                                          schema=WorthLookItemSchema,
                                          client=client,
                                          headers=headers)

        assert is_valid is schema_status
        assert response.status_code == expected_status

    @pytest.mark.parametrize("page_id,expected_status,"
                             "schema_status",
                             [
                                 (
                                         1,
                                         200,
                                         True,
                                 ),
                                 (
                                         'abc',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_get_calendar(self, page_id, expected_status,
                          schema_status):
        response, is_valid = make_request(request_str=f'/{page_id}/calendar/',
                                          schema=CalendarBlockSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is schema_status
        assert response.status_code == expected_status

    def test_get_calendar_block_items(self):
        blocks = CalendarBlockItem.objects.values_list('id', flat=True)
        for block_id in blocks:
            request_str = f'/{block_id}/calendar-items/'
            response, is_valid = make_request(request_str=request_str,
                                              schema=CalendarBlockItemSchema,
                                              client=client,
                                              headers=headers)
            assert is_valid is True
            assert response.status_code == 200

    @pytest.mark.parametrize("tab_id,expected_status,"
                             "schema_status",
                             [
                                 (
                                         1,
                                         200,
                                         True,
                                 ),
                                 (
                                         1000,
                                         404,
                                         False,
                                 ),
                                 (
                                         'abc',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_get_tab_content(self, tab_id, expected_status,
                             schema_status):
        response, is_valid = make_request(request_str=f'/tab-content/{tab_id}/',
                                          schema=TabContentSchema,
                                          client=client,
                                          headers=headers)

        assert is_valid is schema_status
        assert response.status_code == expected_status
