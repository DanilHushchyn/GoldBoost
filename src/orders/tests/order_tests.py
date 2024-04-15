import json
from datetime import timedelta

import pytest
from ninja_extra.testing import TestClient

from src.main.models import PromoCode
from src.main.schemas import OrderOutSchema, PromoCodeSchema
from src.main.utils import make_request
from loguru import logger

from src.orders.api import OrderController
from src.orders.models import Order
from src.orders.schemas import CartOutSchema
from src.products.api import ProductController
from src.products.models import Product
from src.users.models import User
from src.users.schemas import MessageOutSchema, CabinetOrdersSchema
import httpx
from django.utils import timezone

client = TestClient(OrderController)
product_client = TestClient(ProductController)

headers = {
    'Accept-Language': 'en'
}


@pytest.mark.django_db
class TestOrderController:

    @pytest.fixture
    def promo_code(self):
        current_datetime = timezone.now()
        promo = PromoCode.objects.create(**{
            'code': "PYTHON",
            'from_date': current_datetime - timedelta(days=1),
            'until_date': current_datetime + timedelta(days=1),
            'discount': 10,
        })
        return promo

    @pytest.mark.webtest
    def test_get_my_cart(self, access_token):
        rq_str = 'http://127.0.0.1:8000/api/orders/my-cart/'
        response = httpx.get(rq_str, headers=headers)
        assert response.status_code == 200
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-cart/',
                                          schema=CartOutSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is True
        assert response.status_code == 200

    def test_delete_cart_item_404(self, access_token):
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-cart/items/{0}/',
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='delete',
                                          headers=headers)
        assert is_valid is False
        assert response.status_code == 404

    def test_delete_cart_item(self, products_to_cart, access_token):
        count = products_to_cart
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-cart/',
                                          schema=CartOutSchema,
                                          client=client,
                                          headers=headers)

        assert len(response.json()['items']) >= count
        assert response.status_code == 200
        cart_item_id = response.json()['items'][0]['id']
        logger.debug(cart_item_id)
        rq_str = f'my-cart/items/{cart_item_id}/'
        response, is_valid = make_request(request_str=rq_str,
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='delete',
                                          headers=headers)
        assert response.status_code == 200

        response, is_valid = make_request(request_str=f'/my-cart/',
                                          schema=CartOutSchema,
                                          client=client,
                                          headers=headers)
        assert len(response.json()['items']) == count - 1
        assert response.status_code == 200

    def test_create_order(self, products_to_cart, access_token):
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/new/',
                                          schema=OrderOutSchema,
                                          client=client,
                                          method='post',
                                          headers=headers)

        assert is_valid is True
        assert response.status_code == 200

    def test_get_my_orders(self, products_to_cart, access_token):
        self.test_create_order(products_to_cart, access_token)
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-orders/',
                                          schema=CabinetOrdersSchema,
                                          client=client,
                                          headers=headers)

        assert len(response.json()) == 1
        assert is_valid is True
        assert response.status_code == 200

    def test_repeat_my_order(self, products_to_cart, access_token):
        self.test_create_order(products_to_cart, access_token)
        user = User.objects.get(email='user@example.com')
        order = Order.objects.filter(user=user).first()
        headers['Authorization'] = access_token
        rq_str = f'/{order.number}/repeat-order/'
        response, is_valid = make_request(request_str=rq_str,
                                          schema=MessageOutSchema,
                                          method='post',
                                          client=client,
                                          headers=headers)

        assert is_valid is True
        assert response.status_code == 200

    def test_repeat_my_order_404(self, access_token):
        headers['Authorization'] = access_token
        rq_str = f'/{100}/repeat-order/'
        response, is_valid = make_request(request_str=rq_str,
                                          schema=MessageOutSchema,
                                          method='post',
                                          client=client,
                                          headers=headers)

        assert is_valid is False
        assert response.status_code == 404

    def test_check_promo_code(self, promo_code: PromoCode, access_token: str):
        headers['Authorization'] = access_token
        rq_str = f'/check-promo-code/{promo_code.code}/'
        response, is_valid = make_request(request_str=rq_str,
                                          schema=PromoCodeSchema,
                                          method='get',
                                          client=client,
                                          headers=headers)

        assert is_valid is True
        logger.debug(response.json())
        assert response.status_code == 200

    def test_check_promo_code_410(self, promo_code: PromoCode, access_token: str):
        user = User.objects.get(email='user@example.com')
        user.promo_codes.add(promo_code)
        user.save()
        headers['Authorization'] = access_token
        rq_str = f'/check-promo-code/{promo_code.code}/'
        response, is_valid = make_request(request_str=rq_str,
                                          schema=PromoCodeSchema,
                                          method='get',
                                          client=client,
                                          headers=headers)
        assert is_valid is False
        assert response.status_code == 410

    def test_check_promo_code_403(self, promo_code: PromoCode, access_token: str):
        promo_code.until_date = promo_code.from_date
        promo_code.save()
        headers['Authorization'] = access_token
        rq_str = f'/check-promo-code/{promo_code.code}/'
        response, is_valid = make_request(request_str=rq_str,
                                          schema=PromoCodeSchema,
                                          method='get',
                                          client=client,
                                          headers=headers)

        assert is_valid is False
        assert response.status_code == 403
