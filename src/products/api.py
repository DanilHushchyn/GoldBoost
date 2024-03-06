# -*- coding: utf-8 -*-
from typing import List

from django.db.models import QuerySet
from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase, api_controller

from src.games.models import TabItem
from src.main.services.main_service import MainService
from src.products.models import Product
from src.products.schemas import BestSellersSchema, HotSectionSchema, ProductCardSchema, TabContentSchema, TabItemSchema
from src.products.services.product_service import ProductService


@api_controller("/products/", tags=["Product"], permissions=[])
class ProductController(ControllerBase):
    """
    A controller class for managing products.
    This class provides endpoints for ordering, filtering,
    paginating and getting related entities of products.
    """

    def __init__(self, product_service: ProductService, main_service: MainService):
        """
        Use this method to inject services to endpoints of ProductController
        :param product_service: variable for managing products
        :param main_service: variable for managing common entities
        """
        self.product_service = product_service
        self.main_service = main_service

    @http_get("/{product_id}/", response=ProductCardSchema)
    def get_product_by_id(self, product_id: int) -> Product:
        """
        Endpoint gets info for product's card page.
        :param product_id: id of Product model's instance
        :return: Product model's instance with related filters
        """
        result = self.product_service.get_product_by_id(product_id)
        return result

    @http_get("/hot-offers/", response=HotSectionSchema)
    def get_hot_products(self, page: int, page_size: int, game_id: int = 0) -> dict:
        """
        Endpoint gets all products with Tag(related models) value hot
        and make pagination of related queryset
        :rtype: dict
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :param game_id: filter(not required) additionally hot products by game id
        :return: dict which contains all parameters for pagination
        """
        result = self.product_service.get_hot_products(game_id=game_id, page=page, page_size=page_size)
        return result

    @http_get("/bestsellers/", response=BestSellersSchema)
    def get_bestsellers(self, page: int, page_size: int) -> dict:
        """
        Endpoint gets all products ordered by bought_count field in
        model Product (return frequently bought products on site)
        :rtype: object
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains all parameters for pagination
        """
        result = self.product_service.best_sellers(page, page_size)
        return result

    @http_get("/tab/{tab_id}/", response=TabContentSchema)
    def get_tab_content(self, tab_id: int) -> TabItem:
        """
        Endpoint returns specific TabItem model instance
        :rtype: TabItem()
        :param tab_id: id of TabItem model's instance we want to get
        :return: return TabItem() model instance
        """
        result = self.product_service.get_tab_content(tab_id)
        return result

    @http_get("/tabs/{product_id}/", response=List[TabItemSchema])
    def get_product_tabs(self, product_id: int) -> QuerySet:
        """
        Endpoint returns TabItem's queryset filtered
        by id of related Product model's instance
        :rtype: QuerySet
        :param product_id: id of Product model instance
        :return: TabItem's queryset
        """
        result = self.product_service.get_tabs(product_id)
        return result
