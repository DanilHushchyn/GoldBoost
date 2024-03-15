# -*- coding: utf-8 -*-
"""
    Module contains class(set of endpoints) for managing products.

"""
from typing import List
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router
from ninja_extra import http_get, http_post
from ninja_extra.controllers.base import ControllerBase, api_controller
from src.games.models import TabItem
from src.products.models import Product
from src.products.schemas import (BestSellersSchema,
                                  HotSectionSchema, ProductCardSchema,
                                  TabContentSchema,
                                  TabItemSchema, AddToCartSchema)
from src.products.services.product_service import (ProductService,
                                                   get_tab_content)
from src.products.utils import get_current_user
from src.users.schemas import MessageOutSchema


@api_controller("/products/", tags=["Product"], permissions=[])
class ProductController(ControllerBase):
    """
    A controller class for managing products.
    This class provides endpoints for ordering, filtering,
    paginating and getting related entities of products.
    """

    def __init__(self, product_service: ProductService):
        """
        Use this method to inject external services to ProductController.

        :param product_service: variable for managing products
        """
        self.product_service = product_service

    @http_post("/{product_id}/to-cart/", response=MessageOutSchema)
    def add_product_to_cart(self, request: HttpRequest,
                            product_id: int,
                            body: AddToCartSchema) \
            -> MessageOutSchema:
        """
        Endpoint adds product to user's cart.

        :param body: additional attributes for product if it needed
        :param request: HttpRequest()
        :rtype: MessageOutSchema
        :param product_id: the product's id we want to add to cart
        :return: message that product added to cart
        """
        request.session.save()
        user = request.session.session_key
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization']
            user = get_current_user(token=token)
        result = (self.product_service.
                  add_product_to_cart(product_id=product_id,
                                      user=user,
                                      body=body))
        return result

    @http_get("/hot-offers/", response=HotSectionSchema)
    def get_hot_products(self,
                         page: int,
                         page_size: int,
                         game_id: int = 0) -> dict:
        """
        Endpoint gets all products with Tag(related models) value hot.

        Make pagination of related queryset
        :rtype: dict
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :param game_id: filter(not required) additionally by game id
        :return: dict which contains all parameters for pagination
        """
        result = self.product_service.get_hot_products(
            game_id=game_id, page=page, page_size=page_size)
        return result

    @http_get("/bestsellers/", response=BestSellersSchema)
    def get_bestsellers(self, page: int, page_size: int) -> dict:
        """
        Endpoint gets all products ordered by bought_count field.

        Model Product (return frequently bought products on site)
        :rtype: object
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains all parameters for pagination
        """
        result = self.product_service.best_sellers(page, page_size)
        return result

    @http_get("/tabs/{product_id}/", response=List[TabItemSchema])
    def get_product_tabs(self, product_id: int) -> QuerySet:
        """
        Endpoint returns TabItem's queryset filtered by id.

        :rtype: QuerySet
        :param product_id: id of Product model instance
        :return: TabItem's queryset
        """
        result = self.product_service.get_tabs(product_id)
        return result

    @http_get("/{product_id}/", response=ProductCardSchema)
    def get_product_by_id(self, product_id: int) -> Product:
        """
        Endpoint gets info for product's card page.
        :param product_id: id of Product model's instance
        :return: Product model's instance with related filters
        """
        result = self.product_service.get_product_by_id(product_id)
        return result


tab_router = Router(tags=['Tab'])


@tab_router.get("/{tab_id}/tab-content/", response=TabContentSchema)
def get_tab(request: HttpRequest, tab_id: int) -> TabItem:
    """
    Endpoint returns specific TabItem model instance.

    :param request:
    :rtype: TabItem()
    :param tab_id: id of TabItem model's instance we want to get
    :return: return TabItem() model instance
    """

    result = get_tab_content(tab_id)
    return result
