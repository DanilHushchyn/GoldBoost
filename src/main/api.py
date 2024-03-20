# -*- coding: utf-8 -*-
"""
    Module contains class for managing managing common entities on site.

"""
# -*- coding: utf-8 -*-
from typing import List

from django.http import HttpRequest
from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase, api_controller
from ninja_jwt.authentication import JWTAuth

import src.main.schemas as main_schemas
from src.main.models import Insta, Setting, WhyChooseUs
from src.main.services.main_service import MainService
from src.users.schemas import MessageOutSchema


@api_controller("/main", tags=["Main"], permissions=[])
class MainController(ControllerBase):
    """
    A controller class for managing common entities on site.

    This class provides endpoints for ordering, filtering
    and paginating common entities on site.
    """

    def __init__(self, main_service: MainService):
        """
        Use this method to inject services to endpoints of MainController.

        :param main_service: variable for managing common entities
        """
        self.main_service = main_service

    @http_get(
        "/reviews/",
        response=main_schemas.ReviewsSectionSchema,
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
    def get_reviews(self, page: int, page_size: int) -> dict:
        """
        Get data for section Reviews.

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.main_service.get_reviews(page, page_size)
        return result

    @http_get(
        "/why-choose-us/",
        response=List[main_schemas.WhyChooseUsSchema],
        openapi_extra={
            "responses": {
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_why_choose_us(self) -> WhyChooseUs:
        """
        Get data for section WhyChooseUs.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.main_service.get_why_choose_us()
        return result

    @http_get(
        "/instagram/",
        response=List[main_schemas.InstaSchema],
        openapi_extra={
            "responses": {
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_instagram(self) -> Insta:
        """
        Get data for section Instagram.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.main_service.get_instagram()
        return result

    @http_get(
        "/news/",
        response=main_schemas.NewsSectionSchema,
        openapi_extra={
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
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_news(self, page: int, page_size: int) -> dict:
        """
        Get data for section News.

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.main_service.get_news(page, page_size)
        return result

    @http_get(
        "/settings/",
        response=main_schemas.SettingsOutSchema,
        openapi_extra={
            "responses": {
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_settings(self) -> Setting:
        """
        Get data for footer and header of the site.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.main_service.get_settings()
        return result

    @http_get(
        "/check-promo-code/{code}/",
        response=main_schemas.PromoCodeSchema,
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
                                "example": {"detail": "Promo code " "has been expired ☹"},
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
                                "example": {"detail": "Promo code " "has been already used ☹"},
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
    def check_promo_code(self, request: HttpRequest, code: str) -> MessageOutSchema:
        """
        Check promo code.

        Please provide:
         - **code**  code we want to check

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **403**: Promo code has been already used.
          - **410**: Promo code has been expired.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.main_service.check_promo_code(code=code, user=request.user)
        return result
