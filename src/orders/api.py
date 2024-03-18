# -*- coding: utf-8 -*-
"""
    Module contains class(set of endpoints) for managing orders and carts.
"""
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra import http_get, http_delete, http_post
from ninja_jwt.authentication import JWTAuth

from src.main.schemas import OrderOutSchema
from src.orders.models import Cart, Order
from src.orders.schemas import CartOutSchema, CreateOrderInSchema
from src.orders.services.order_service import OrderService
from src.products.utils import get_current_user
from src.users.schemas import MessageOutSchema, CabinetOrdersSchema
from src.users.utils import OptionalJWTAuth


@api_controller("/orders/", tags=["Orders"], permissions=[])
class OrderController(ControllerBase):
    """
    A controller class for managing orders and carts.
    This class provides endpoints for ordering, filtering,
    paginating and getting related entities of orders.
    """

    def __init__(self, order_service: OrderService):
        """
        Use this method to inject services to endpoints of OrderController.

        """
        self.order_service = order_service

    @http_get("/my-cart/", response=CartOutSchema,
              auth=OptionalJWTAuth(),
              summary='Get my cart (OPTIONAL Auth)')
    def get_my_cart(self, request: HttpRequest) \
            -> Cart:
        """
        Endpoint gets  user's cart.

        :param request: HttpRequest()
        :rtype: CartOutSchema
        :return: cart's products
        """
        request.session.save()
        user = request.session.session_key
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization']
            user = get_current_user(token=token)
        result = self.order_service.get_my_cart(user=user, )
        return result

    @http_delete("/my-cart/items/{item_id}/", response=MessageOutSchema,
                 auth=OptionalJWTAuth(),
                 summary="Delete cart's item (OPTIONAL Auth)")
    def delete_cart_item(self, request: HttpRequest, item_id: int) \
            -> Cart:
        """
        Endpoint delete cart's item.

        :param item_id: cart's item id
        :param request: HttpRequest()
        :rtype: MessageOutSchema
        :return: message that item deleted
        """
        request.session.save()
        user = request.session.session_key
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization']
            user = get_current_user(token=token)
        result = (self.order_service.
                  delete_cart_item(user=user, item_id=item_id))
        return result

    @http_post("/new/", response=OrderOutSchema, auth=OptionalJWTAuth(),
               summary="Create new order (OPTIONAL Auth)")
    def create_order(self, request: HttpRequest, promo_code: str|None = None) \
            -> OrderOutSchema:
        """
        Endpoint creates order.

        :param promo_code: for order if exists
        :param request: HttpRequest()
        :return: result of operation
        """
        request.session.save()
        user = request.session.session_key
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization']
            user = get_current_user(token=token)
        result = self.order_service.create_order(user=user, promo_code=promo_code)
        return result

    @http_post("/{order_id}/repeat-order/",
               response=CabinetOrdersSchema, auth=JWTAuth())
    def repeat_order(self, request: HttpRequest, order_id: str) \
            -> Order:
        """
        Endpoint repeat order.

        :param order_id: order's id
        :param request: HttpRequest()
        :return: result of operation
        """
        result = (self.order_service.
                  repeat_order(user=request.user,
                               order_id=order_id))
        return result

    @http_get("/my-orders/", response=list[CabinetOrdersSchema],
              auth=JWTAuth())
    def get_my_orders(self, request: HttpRequest) \
            -> QuerySet:
        """
        Endpoint get user's orders.

        :param request: HttpRequest()
        :return: result of operation
        """
        result = self.order_service.get_my_orders(user_id=request.user.id)
        return result
