# -*- coding: utf-8 -*-
"""
    Module contains class(set of endpoints) for managing products.

"""
from typing import List

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja.params.functions import Header
from ninja_extra import http_get, http_post
from ninja_extra.controllers.base import ControllerBase, api_controller

from src.main.utils import LangEnum
from src.orders.services.order_service import OrderService
from src.products.models import Product, ProductTabs
from src.products.schemas import (
    AddToCartSchema,
    BestSellersSchema,
    HotSectionSchema,
    ProductCardSchema,
    ProductSearchSchema,
    TabContentSchema, FreqBoughtSchema,
)
from src.products.services.product_service import ProductService
from src.products.utils import get_current_user
from src.users.schemas import MessageOutSchema
from src.users.utils import OptionalJWTAuth


@api_controller("/products/", tags=["Product"], permissions=[])
class ProductController(ControllerBase):
    """
    A controller class for managing products.

    This class provides endpoints for ordering, filtering,
    paginating and getting related entities of products.
    """

    def __init__(self, product_service: ProductService,
                 order_service: OrderService):
        """
        Use this method to inject external services to ProductController.

        :param product_service: variable for managing products
        """
        self.product_service = product_service
        self.order_service = order_service

    @http_post(
        "/{product_id}/to-cart/",
        response=MessageOutSchema,
        auth=OptionalJWTAuth(),
        summary="Add product to cart (OPTIONAL Auth)",
        openapi_extra={
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {
                            "properties": {
                                "attributes": {
                                    "type": "array",
                                },
                                "quantity": {
                                    "type": "int",
                                    "default": 1,
                                },
                            },
                        }
                    },
                },
                "required": True,
            },
            "responses": {
                401: {
                    "description": "ERROR: Unauthorized",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Unauthorized"},
                            }
                        }
                    },
                },
                404: {
                    "description": "Error: Not Found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Not Found: " "No Product matches " "the given query."},
                            }
                        }
                    },
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def add_product_to_cart(self,
                            request: HttpRequest,
                            product_id: int,
                            body: AddToCartSchema,
                            accept_lang:
                            LangEnum = Header(alias='Accept-Language'),
                            ) -> MessageOutSchema:
        """
        Add product to user's cart

        Please provide:
         - **product_id**  id of product we want to add to cart
         - **Request body**  specify product's parameters

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        if not request.auth.is_anonymous:
            user = request.auth
        else:
            # request.session.save()
            user = request.session.session_key
        result = self.product_service.add_product_to_cart(product_id=product_id, user=user, body=body)
        return result

    @http_post(
        "/freqbot/{freqbot_id}/to-cart/",
        response=MessageOutSchema,
        auth=OptionalJWTAuth(),
        openapi_extra={
            401: {
                "description": "ERROR: Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {
                            "properties": {
                                "detail": {
                                    "type": "string",
                                }
                            },
                            "example": {"detail": "Unauthorized"},
                        }
                    }
                },
            },
            404: {
                "description": "Error: Not Found",
                "content": {
                    "application/json": {
                        "schema": {
                            "properties": {
                                "detail": {
                                    "type": "string",
                                }
                            },
                            "example": {"detail": "Not Found: " "No FreqBought matches " "the given query."},
                        }
                    }
                },
            },
            422: {
                "description": "Error: Unprocessable Entity",
                "content": {
                    "application/json": {
                        "schema": {
                            "properties": {
                                "detail": {
                                    "type": "string",
                                }
                            },
                        }
                    }
                },
            },
            "responses": {
                500: {
                    "description": "Internal server error if"
                                   " an unexpected error occurs.",
                },
            },
        },
    )
    def freqbot_to_cart(self,
                        request: HttpRequest,
                        freqbot_id: int,
                        accept_lang:
                        LangEnum = Header(alias='Accept-Language'),
                        ) -> QuerySet:
        """
        Add Frequently bought item to cart.


        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        if not request.auth.is_anonymous:
            user = request.auth
        else:
            request.session.save()
            user = request.session.session_key
        cart = self.order_service.get_my_cart(user)
        result = self.product_service.freqbot_to_cart(freqbot_id, cart)
        return result

    @http_get(
        "/hot-offers/",
        response=HotSectionSchema,
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if"
                                   " an unexpected error occurs.",
                },
            },
        },
    )
    def get_hot_products(self, request: HttpRequest,
                         page: int,
                         page_size: int,
                         game_id: int = None,
                         accept_lang:
                         LangEnum = Header(alias='Accept-Language'),
                         ) -> dict:
        """
        Get all products with tag hot and makes pagination of records.

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page
         - **game_id**  id of game for filtering(it's optional)

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.product_service.get_hot_products(game_id=game_id, page=page, page_size=page_size)
        return result

    @http_get(
        "/bestsellers/",
        response=BestSellersSchema,
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if"
                                   " an unexpected error occurs.",
                },
            },
        },
    )
    def get_bestsellers(self, request: HttpRequest, page: int,
                        page_size: int,
                        accept_lang:
                        LangEnum = Header(alias='Accept-Language'),
                        ) -> dict:
        """
        Endpoint gets all products ordered by bought_count field.

        Makes pagination of records.

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.product_service.best_sellers(page, page_size)
        return result

    @http_get(
        "/freqbot-section/",
        response=List[FreqBoughtSchema],
        openapi_extra={
            "responses": {
                500: {
                    "description": "Internal server error if"
                                   " an unexpected error occurs.",
                },
            },
        },
    )
    def frequently_bought(self, request: HttpRequest,
                          accept_lang:
                          LangEnum = Header(alias='Accept-Language'),
                          ) -> QuerySet:
        """
        Endpoint gets all products ordered by bought_count field.

        Makes pagination of records.


        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.product_service.frequently_bought()
        return result

    @http_get(
        "tab-content/{tab_id}/",
        response=TabContentSchema,
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Not Found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Not Found: " "No ProductTabs matches " "the given query."},
                            }
                        }
                    },
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_tab_content(self, request: HttpRequest, tab_id: int,
                        accept_lang:
                        LangEnum = Header(alias='Accept-Language'),
                        ) -> ProductTabs:
        """
        Get tab's content for product's page by tab id .

        Please provide:
         - **tab_id**  id of tab we want to get

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.product_service.get_tab_content(tab_id=tab_id)
        return result

    @http_get(
        "/search/",
        response=List[ProductSearchSchema],
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def search_products(self, request: HttpRequest,
                        search_line: str,
                        game_id: int = None,
                        accept_lang:
                        LangEnum = Header(alias='Accept-Language'),
                        ) -> QuerySet:
        """
        Get records of products searched by search_line.

        Please provide:
         - **search_line**  id of tab we want to get
         - **game_id**  id of game by which we want to filter records

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.product_service.search_products(game_id=game_id, search_line=search_line)
        return result

    @http_get(
        "/{product_id}/",
        response=ProductCardSchema,
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Not Found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Not Found: " "No Product matches " "the given query."},
                            }
                        }
                    },
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_product_by_id(self, request: HttpRequest,
                          product_id: int,
                          accept_lang:
                          LangEnum = Header(alias='Accept-Language'),
                          ) -> Product:
        """
        Gets info for product's card page.

        Please provide:
         - **product_id**  id of product we want to get

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.product_service.get_product_by_id(request, product_id)
        return result
