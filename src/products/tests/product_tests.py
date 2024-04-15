import json

import pytest
from django.test import TestCase
from ninja_extra.testing import TestClient
from src.main.utils import make_request
from loguru import logger

from src.orders.api import OrderController
from src.products.api import ProductController
from src.products.schemas import *
from src.users.schemas import MessageOutSchema
import httpx

client = TestClient(ProductController)
orders_client = TestClient(OrderController)

headers = {
    'Accept-Language': 'en'
}


@pytest.mark.django_db
class TestProductController:

    @pytest.mark.parametrize("product_id,expected_status,schema_status",
                             [
                                 (
                                         1,
                                         200,
                                         True,
                                 ),
                                 (
                                         0,
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
    def test_get_product_by_id(self, product_id, expected_status,
                               schema_status):
        response, is_valid = make_request(request_str=f'/{product_id}/',
                                          schema=ProductCardSchema,
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
    def test_get_bestsellers(self, payload, expected_status,
                             schema_status):
        request_str = f'/bestsellers/{payload}'
        response, is_valid = make_request(request_str=request_str,
                                          schema=BestSellersSchema,
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
                                         '?page=1&page_size=4&game_id=1',
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
    def test_get_hot_offers(self, payload, expected_status,
                            schema_status):
        request_str = f'/hot-offers/{payload}'
        response, is_valid = make_request(request_str=request_str,
                                          schema=HotSectionSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is schema_status
        assert response.status_code == expected_status

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
        request_str = f'/tab-content/{tab_id}/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=TabContentSchema,
                                          client=client,
                                          headers=headers)

        assert is_valid is schema_status
        assert response.status_code == expected_status

    @pytest.mark.parametrize("payload,expected_status,schema_status",
                             [
                                 (
                                         '?search_line=war&game_id=1',
                                         200,
                                         True,

                                 ),
                                 (
                                         '?search_line=war',
                                         200,
                                         True,

                                 ),
                                 (
                                         '',
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_search_products(self, payload, expected_status,
                             schema_status):
        request_str = f'/search/{payload}'
        response, is_valid = make_request(request_str=request_str,
                                          schema=ProductSearchSchema,
                                          client=client,
                                          headers=headers)

        assert is_valid is schema_status
        assert response.status_code == expected_status

    def test_add_freqbot_to_cart(self, access_token):
        headers['Authorization'] = access_token

        freqbot = FreqBought.objects.first()
        request_str = f'/freqbot/{freqbot.id}/to-cart/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='post',
                                          headers=headers)

        assert is_valid is True
        assert response.status_code == 200

    def test_freqbot_section(self, ):
        request_str = f'/freqbot-section/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=FreqBoughtSchema,
                                          client=client,
                                          headers=headers)

        assert is_valid is True
        assert response.status_code == 200

    @pytest.mark.parametrize("freqbot_id,expected_status,schema_status",
                             [
                                 (
                                         0,
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
    def test_errors_add_freqbot_to_cart(self, freqbot_id,
                                        expected_status, schema_status):
        request_str = f'/freqbot/{freqbot_id}/to-cart/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='post',
                                          headers=headers)

        assert is_valid is schema_status
        assert response.status_code == expected_status

    # @pytest.mark.parametrize("attributes,expected_status,schema_status",
    #                          [
    #                              (
    #                                      [101, 202, 303, 404],
    #                                      200,
    #                                      True,
    #
    #                              ),
    # (
    #         [101, 202, 404],
    #         200,
    #         True,
    # ),
    # (
    #         [101, 202, 303, 304, 305, 404],
    #         200,
    #         True,
    # ),
    # (
    #         [202, 203, 404],
    #         403,
    #         False,
    # ),
    # (
    #         [202, 404],
    #         403,
    #         False,
    # ),
    # (
    #         [303, 404],
    #         403,
    #         False,
    # ),
    # ]
    # )
    # def test_add_product_to_cart(self, attributes, expected_status,
    #                              schema_status, product_with_range:Product,
    #                              access_token):
    #     request_str = f'/{product_with_range.id}/to-cart/'
    #     payload = {
    #         'attributes': attributes,
    #         'quantity': 1,
    #     }
    #     logger.debug(list(SubFilter.objects.values_list('id',flat=True)))
    #     headers['Authorization'] = access_token
    #     response, is_valid = make_request(request_str=request_str,
    #                                       schema=MessageOutSchema,
    #                                       client=client,
    #                                       method='post',
    #                                       payload=json.dumps(payload),
    #                                       headers=headers)
    #     logger.debug(response.json())
    #     assert is_valid is schema_status
    #     assert response.status_code == expected_status

    def test_add_product_fixed_to_cart(self, products_to_cart,
                                       access_token):
        count = products_to_cart
        headers['Authorization'] = access_token
        request_str = f'/my-cart/'
        response, is_valid = make_request(request_str=request_str,
                                          schema=MessageOutSchema,
                                          client=orders_client,
                                          method='get',
                                          headers=headers)
        assert len(response.json()['items']) == count
        assert response.status_code == 200

    def test_add_product_fixed_to_cart_404(self, access_token):
        request_str = f'/{0}/to-cart/'
        payload = {
            'attributes': [],
            'quantity': 1,
        }
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=request_str,
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='post',
                                          payload=json.dumps(payload),
                                          headers=headers)
        assert is_valid is False
        assert response.status_code == 404
