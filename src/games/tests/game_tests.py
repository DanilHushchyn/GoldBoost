import pytest
from ninja_extra.testing import TestClient
from jsonschema import validate
from src.games.api import GamesController
import jsonschema

from src.games.schemas import *
from src.main.utils import make_request
from src.products.schemas import GameCarouselsMainSchema

client = TestClient(GamesController)
headers = {
    'Accept-Language': 'en'
}


@pytest.mark.django_db
class TestGameController:

    def test_get_games(self):
        response, is_valid = make_request(request_str=f'/',
                                          schema=GamesSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is True
        assert response.status_code == 200

    @pytest.mark.parametrize("game_id,expected_status,"
                             "schema_status",
                             [
                                 (
                                         1,
                                         200,
                                         True,
                                 ),
                                 (
                                         100,
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
    def test_get_game_pages(self, game_id, expected_status,
                            schema_status):
        request_str = f'/{game_id}/catalog-pages/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=SidebarSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is schema_status
        assert response.status_code == expected_status

    @pytest.mark.parametrize("query_str,expected_status,"
                             "schema_status",
                             [
                                 (
                                         'page=1'
                                         '&page_size=4'
                                         '&game_id=1'
                                         '&catalog_id=2',
                                         200,
                                         True,
                                 ),
                                 (
                                         'page=1'
                                         '&page_size=4'
                                         '&game_id=1',
                                         200,
                                         True,
                                 ),
                                 (
                                         'page=1',
                                         422,
                                         False,
                                 ),
                                 (
                                         'page=1'
                                         '&page_size=4',
                                         422,
                                         False,
                                 ),
                                 (
                                         'page=1'
                                         '&game_id=1',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_get_game_products(self, query_str, expected_status,
                               schema_status):
        request_str = f'/product-carousels/?{query_str}'
        response, is_valid = make_request(request_str=request_str,
                                          schema=GameCarouselsMainSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is schema_status
        assert response.status_code == expected_status
