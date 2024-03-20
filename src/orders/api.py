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
              summary='Get my cart (OPTIONAL Auth)',
              openapi_extra={
                  "responses": {
                    401: {
                          "description": "Error: Unauthorized",
                          "content": {
                              "application/json": {
                                  "schema": {
                                      "properties": {
                                          "detail": {
                                              "type": "string",
                                              "default": "Unauthorized",
                                          }
                                      },
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
    def get_my_cart(self, request: HttpRequest) \
            -> Cart:
        """
        Get  user's cart.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **500**: Internal server error if an unexpected error occurs.
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
                 summary="Delete cart's item (OPTIONAL Auth)",
                 openapi_extra={
                     "responses": {
                         401: {
                             "description": "Error: Unauthorized",
                             "content": {
                                 "application/json": {
                                     "schema": {
                                         "properties": {
                                             "detail": {
                                                 "type": "string",
                                                 "default": "Unauthorized",
                                             }
                                         },
                                     }
                                 }
                             },
                         },
                         404: {
                             "description": "Error: Unauthorized",
                             "content": {
                                 "application/json": {
                                     "schema": {
                                         "properties": {
                                             "detail": {
                                                 "type": "string",
                                                 "default": "Not Found: "
                                                            "No CartItem "
                                                            "matches the "
                                                            "given query"
                                                            ".",
                                             }
                                         },
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
    def delete_cart_item(self, request: HttpRequest, item_id: int) \
            -> Cart:
        """
        Delete cart's item.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **404**: ERROR: Not Found.
          - **500**: Internal server error if an unexpected error occurs.
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
               summary="Create new order (OPTIONAL Auth)",
               openapi_extra={
                   "responses": {
                       401: {
                           "description": "Error: Unauthorized",
                           "content": {
                               "application/json": {
                                   "schema": {
                                       "properties": {
                                           "detail": {
                                               "type": "string",
                                               "default": "Unauthorized",
                                           }
                                       },
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
                                               "default": "Your cart"
                                                          " is empty ☹",
                                           }
                                       },
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
    def create_order(self, request: HttpRequest, promo_code: str | None = None) \
            -> OrderOutSchema:
        """
        Create order.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **404**: ERROR: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        request.session.save()
        user = request.session.session_key
        if 'Authorization' in request.headers.keys():
            token = request.headers['Authorization']
            user = get_current_user(token=token)
        result = self.order_service.create_order(user=user, promo_code=promo_code)
        return result

    @http_post("/{order_id}/repeat-order/",
               response=CabinetOrdersSchema, auth=JWTAuth(),
               openapi_extra={
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
                                       "example": {
                                           "detail": "Unauthorized"
                                       }

                                   }
                               }
                           },

                       },
                       404: {
                           "description": "ERROR: Not Found",
                           "content": {
                               "application/json": {
                                   "schema": {
                                       "properties": {
                                           "detail": {
                                               "type": "string",
                                           }
                                       },
                                       "example": {
                                           "detail": "Cannot repeat "
                                                     "order, some "
                                                     "products are not"
                                                     " exists nowadays ☹"
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
    def repeat_order(self, request: HttpRequest, order_id: str) \
            -> Order:
        """
        Repeat order.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **404**: ERROR: Not Found.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = (self.order_service.
                  repeat_order(user=request.user,
                               order_id=order_id))
        return result

    @http_get("/my-orders/", response=list[CabinetOrdersSchema],
              auth=JWTAuth(),
              openapi_extra={
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
                                      "example": {
                                          "detail": "Unauthorized"
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
    def get_my_orders(self, request: HttpRequest) \
            -> QuerySet:
        """
        Get user's orders.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.order_service.get_my_orders(user_id=request.user.id)
        return result
