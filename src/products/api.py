# -*- coding: utf-8 -*-
"""
    Module contains class(set of endpoints) for managing products.

"""
from typing import List

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra import http_get, http_post
from ninja_extra.controllers.base import ControllerBase, api_controller
from src.products.models import Product, ProductTabs
from src.products.schemas import (BestSellersSchema,
                                  HotSectionSchema, ProductCardSchema,
                                  AddToCartSchema, TabContentSchema, ProductSearchSchema)
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

    def __init__(self, product_service: ProductService):
        """
        Use this method to inject external services to ProductController.

        :param product_service: variable for managing products
        """
        self.product_service = product_service

    @http_post("/{product_id}/to-cart/", response=MessageOutSchema,
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
                                       }
                                   }, }
                           },
                       },
                       "required": True
                   },
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
                                       "example": {
                                           "detail":
                                               "Not Found: "
                                               "No Product matches "
                                               "the given query."
                                       }

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
                           "description": "Internal server error if"
                                          " an unexpected error occurs.",
                       },
                   },
               }, )
    def add_product_to_cart(self, request: HttpRequest,
                            product_id: int,
                            body: AddToCartSchema) \
            -> MessageOutSchema:
        """
        Add product to user's cart

        Please provide:
         - **product_id**  id of product we want to add to cart
         - **Request body**  specify product's parameters

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
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

    @http_get("/hot-offers/", response=HotSectionSchema,
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
              }, )
    def get_hot_products(self,
                         page: int,
                         page_size: int,
                         game_id: int = None) -> dict:
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
        result = self.product_service.get_hot_products(
            game_id=game_id, page=page, page_size=page_size)
        return result

    @http_get("/bestsellers/", response=BestSellersSchema,
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
              }, )
    def get_bestsellers(self, page: int, page_size: int) -> dict:
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

    @http_get("tab-content/{tab_id}/", response=TabContentSchema,
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
                                      "example": {
                                          "detail":
                                              "Not Found: "
                                              "No ProductTabs matches "
                                              "the given query."
                                      }

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
                          "description": "Internal server error if"
                                         " an unexpected error occurs.",
                      },
                  },
              }, )
    def get_tab_content(self, request: HttpRequest, tab_id: int) \
            -> ProductTabs:
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

    @http_get("/search/", response=List[ProductSearchSchema],
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
              }, )
    def search_products(self, request: HttpRequest,
                        search_line: str, game_id: int = None) \
            -> QuerySet:
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
        result = (self.product_service.
                  search_products(game_id=game_id,
                                  search_line=search_line))
        return result

    @http_get("/{product_id}/", response=ProductCardSchema,
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
                                      "example": {
                                          "detail":
                                              "Not Found: "
                                              "No Product matches "
                                              "the given query."
                                      }

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
                          "description": "Internal server error if"
                                         " an unexpected error occurs.",
                      },
                  },
              }, )
    def get_product_by_id(self, product_id: int) -> Product:
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
        result = self.product_service.get_product_by_id(product_id)
        return result
