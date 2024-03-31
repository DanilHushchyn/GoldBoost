# -*- coding: utf-8 -*-
"""
    Module contains class(set of endpoints) for managing orders and carts.
"""
from typing import Annotated

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra import http_delete, http_get, http_post
from ninja_extra.controllers.base import ControllerBase, api_controller
from ninja_jwt.authentication import JWTAuth

from src.main.models import PromoCode
from src.main.schemas import OrderOutSchema, PromoCodeSchema
from src.main.utils import LangEnum
from src.orders.models import Cart, Order
from src.orders.schemas import CartOutSchema, CreateOrderInSchema
from src.orders.services.order_service import OrderService
from src.products.utils import get_current_user
from src.users.schemas import CabinetOrdersSchema, MessageOutSchema
from src.users.utils import OptionalJWTAuth
from ninja import Header


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

    @http_get(
        "/my-cart/",
        response=CartOutSchema,
        auth=OptionalJWTAuth(),
        summary="Get my cart (OPTIONAL Auth)",
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
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_my_cart(self, request: HttpRequest,
                    accept_lang:
                    LangEnum = Header(alias='Accept-Language'),
                    ) -> Cart:
        """
        Get  user's cart.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **500**: Internal server error if an unexpected error occurs.
        """
        if not request.auth.is_anonymous:
            user = request.auth
        else:
            request.session.save()
            user = request.session.session_key

        result = self.order_service.get_my_cart(
            user=user,
        )
        return result

    @http_delete(
        "/my-cart/items/{item_id}/",
        response=MessageOutSchema,
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
                                        "default": "Not Found: " "No CartItem " "matches the " "given query" ".",
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
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def delete_cart_item(self, request: HttpRequest, item_id: int,
                         accept_lang:
                         LangEnum = Header(alias='Accept-Language'),
                         ) -> Cart:
        """
        Delete cart's item.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **404**: ERROR: Not Found.
          - **500**: Internal server error if an unexpected error occurs.
        """
        if not request.auth.is_anonymous:
            user = request.auth
        else:
            request.session.save()
            user = request.session.session_key
        result = self.order_service.delete_cart_item(user=user, item_id=item_id)
        return result

    @http_post(
        "/new/",
        response=OrderOutSchema,
        auth=OptionalJWTAuth(),
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
                400: {
                    "description": "Error: Bad Request",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                        "default": "Your cart is empty",
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
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def create_order(self, request: HttpRequest, promo_code: str | None = None,
                     accept_lang:
                     LangEnum = Header(alias='Accept-Language'),
                     ) -> OrderOutSchema:
        """
        Create order.

        Returns:
          - **200**: Success response with the data.
          - **400**: ERROR: Bad Request.
          - **404**: ERROR: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        if not request.auth.is_anonymous:
            user = request.auth
        else:
            request.session.save()
            user = request.session.session_key
        result = self.order_service.create_order(user=user, code=promo_code)
        return result

    @http_get(
        "/check-promo-code/{promo_code}/",
        response=PromoCodeSchema,
        auth=JWTAuth(),
        openapi_extra={
            "responses": {
                401: {
                    "description": "Unauthorized",
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
                403: {
                    "description": "Promo code has been expired",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Promo code " "has been expired"},
                            }
                        }
                    },
                },
                410: {
                    "description": "Promo code " "has been already used",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Promo code " "has been already used"},
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
    def check_promo_code(self, request: HttpRequest, promo_code: str,
                         accept_lang:
                         LangEnum = Header(alias='Accept-Language'),
                         ) -> PromoCode:
        """
        Check promo code.

        Please provide:
         - **code**  code we want to check

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **403**: Promo code has been expired.
          - **410**: Promo code has been already used.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.order_service.check_promo_code(code=promo_code, user=request.user)
        return result

    @http_post(
        "/{number}/repeat-order/",
        response=MessageOutSchema,
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
                                "example": {"detail": "Unauthorized"},
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
                                    "detail": "Cannot repeat " "order, some " "products are not" " exists nowadays"
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
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def repeat_order(self, request: HttpRequest, number: str,
                     accept_lang:
                     LangEnum = Header(alias='Accept-Language'),
                     ) -> MessageOutSchema:
        """
        Repeat order.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **404**: ERROR: Not Found.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.order_service.repeat_order(user=request.user, number=number)
        return result

    @http_get(
        "/my-orders/",
        response=list[CabinetOrdersSchema],
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
                                "example": {"detail": "Unauthorized"},
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
    def get_my_orders(self, request: HttpRequest,
                      accept_lang:
                      LangEnum = Header(alias='Accept-Language'),
                      ) -> QuerySet:
        """
        Get user's orders.

        Returns:
          - **200**: Success response with the data.
          - **401**: ERROR: Unauthorized.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.order_service.get_my_orders(user_id=request.user.id)
        return result
