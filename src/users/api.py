# -*- coding: utf-8 -*-
"""
    Module contains class for managing users in the site
"""
import json

from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialLogin
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Header
from ninja_extra import http_delete, http_get, http_patch, http_post
from ninja_extra.controllers.base import ControllerBase, api_controller
from ninja_extra.permissions.common import AllowAny
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings

from src.main.utils import LangEnum
from src.users.schemas import *
from src.users.schemas import MessageOutSchema
from src.users.services.auth_service import AuthService
from src.users.services.user_service import UserService

@api_controller("/users", tags=["Users"])
class UsersController(ControllerBase):
    """
    A controller class for managing users.

    using in cabinet(subdomain's private part of site).
    """

    def __init__(self, user_service: UserService):
        """
        Use this method to inject "services" to endpoints.

        :param user_service: variable for managing user's data in system
        """
        self.user_service = user_service

    @http_post(
        "/subscribe/",
        response=MessageOutSchema,
        openapi_extra={
            "responses": {
                200: {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "default": "You are " "successfully " "subscribed",
                                    }
                                },
                            }
                        }
                    },
                },
                409: {
                    "description": "Error: Conflict",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                        "default": "This email" " has been " "already " "subscribed",
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
    def subscribe(
        self,
        request: HttpRequest,
        body: EmailSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> MessageOutSchema:
        """
        Subscribe user to news by user's email

        Please provide:
         - **RequestBody**  email of user we want to subscribe for news

        Returns:
          - **200**: Success response with the data.
          - **409**: This email has been already subscribed.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.user_service.subscribe(body=body)
        return result

    @http_patch(
        "/my-profile/",
        response=UserUpdatedSchema,
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
    def update_my_profile(
        self,
        request: HttpRequest,
        user_body: UserInSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> User:
        """
        Update user's personal data.
        Please provide:
         - **Request body**  schema with fields for updating profile

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.user_service.update_my_profile(request.user.id, user_body)
        return result

    @http_get(
        "/my-profile/",
        response=UserOutSchema,
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
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_my_profile(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> User:
        """
        Get user's personal data for cabinet.

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.get_my_profile(request.user.id)
        return result

    @http_post(
        "/create-default-character/",
        response=CharacterOutSchema,
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
                409: {
                    "description": "Error: Conflict",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                        "default": "Not more " "than 3 " "characters " "are possible " "to create",
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
    def create_default_character(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> Character:
        """
        Create default user's characters.

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **409**: Error: Conflict.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.user_service.create_character(request.user.id)
        return result

    @http_delete(
        "/my-character/{character_id}",
        response=MessageOutSchema,
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
                                "example": {"detail": "Not Found: " "No Character " "matches the " "given query."},
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
    def delete_character_by_id(
        self,
        request: HttpRequest,
        character_id: int,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> MessageOutSchema:
        """
        Delete user's character by id.
        Please provide:
          - **character_id**  id of character for deleting

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.user_service.delete_character_by_id(character_id)
        return result

    @http_patch(
        "/my-character/{character_id}",
        response=CharacterOutSchema,
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
                                "example": {"detail": "Not Found: " "No Character " "matches the " "given query."},
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
    def update_character_by_id(
        self,
        request: HttpRequest,
        character_id: int,
        character: CharacterInSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> Character:
        """
        Update user's character by id.

        Please provide:
          - **character_id**  id of character for updating
          - **Request body**  schema with fields for update

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.user_service.update_character_by_id(character_id, character)

        return result

    @http_get(
        "/my-characters/",
        response=list[CharacterOutSchema],
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
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_my_characters(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> QuerySet:
        """
        Get records of user's characters.

        Returns:
          - **200**: Success response with the data.
          - **401**: Unauthorized.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.get_my_characters(request.user.id)
        return result


@api_controller("/auth", tags=["token"])
class AuthController(ControllerBase):
    """
    A controller class for managing access control system on site.

    This class provides endpoints for registration,login,
    reset password and so on
    """

    def __init__(self, auth_service: AuthService):
        """
        Use this method to inject "services" to AuthController.

        :param auth_service: variable for managing access control system
        """
        self.auth_service = auth_service

    @http_post(
        "/registration/",
        tags=["token"],
        response=MessageOutSchema,
        openapi_extra={
            "responses": {
                409: {
                    "description": "Error: Conflict",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "This email already" " in use"},
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
    def registration(
        self,
        request: HttpRequest,
        user: RegisterSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> MessageOutSchema:
        """
        Register new user.

        Please provide:
          - **Request body**  data for registration new user

        Returns:
          - **200**: Success response with the data.
          - **409**: Error: Conflict.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.auth_service.register_user(user_body=user)
        return result

    @http_post(
        "/google-login",
        response=SocialAccountSchema,
        auth=None,
    )
    def google_login(self, request, payload: SocialLoginSchema):
        try:
            app = SocialApp.objects.get(name="Google")
        except SocialApp.DoesNotExist:
            return 404, {"message": "Google app does not exist"}
        adapter = GoogleOAuth2Adapter(request)
        return self.auth_service.social_login(request, app, adapter, payload.access_token)

    @http_post(
        "/reset-password/",
        tags=["token"],
        openapi_extra={
            "responses": {
                409: {
                    "description": "Error: Conflict",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "This email already" " in use"},
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
    def reset_password(
        self,
        request: HttpRequest,
        body: EmailSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> MessageOutSchema:
        """
        Reset user's password.

        Part 1
        Please provide:
          - **Request body**  email where will be sent letter
           for confirm email with details for Part 2
        Returns:
          - **200**: Success response with the data.
          - **409**: Error: Conflict.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.auth_service.reset_password(body=body)
        return result

    @http_post(
        "/check-change-password/",
        tags=["token"],
        openapi_extra={
            "responses": {
                400: {
                    "description": "Error: Invalid data provided",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Invalid link"},
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
    def check_change_password(
        self,
        request: HttpRequest,
        body: ConfirmationSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> MessageOutSchema:
        """
        Check data for reset user's password.

        Please provide:
          - **Request body**  data which we want to check

        Returns:
          - **200**: Success response with the data.
          - **400**: Error: Invalid data provided.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.auth_service.check_change_password(body=body)
        return result

    @http_post(
        "/change-password/",
        tags=["token"],
        openapi_extra={
            "responses": {
                400: {
                    "description": "Error: Invalid data provided",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Invalid link"},
                            }
                        }
                    },
                },
                403: {
                    "description": "Error: Forbidden",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Passwords aren't the same"},
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
    def change_password(
        self,
        request: HttpRequest,
        body: ChangePasswordSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> MessageOutSchema:
        """
        Change user's password.

        Part 2
        Please provide:
          - **Request body**  data with new passwords and credentials

        Returns:
          - **200**: Success response with the data.
          - **400**: Error: Invalid data provided.
          - **403**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.auth_service.change_password(body=body)
        return result

    @http_post(
        "/confirm-email/",
        tags=["token"],
        openapi_extra={
            "responses": {
                400: {
                    "description": "Error: Invalid data provided",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Invalid link"},
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
    def confirm_email(
        self,
        request: HttpRequest,
        body: ConfirmationSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language"),
    ) -> MessageOutSchema:
        """
        Activate user account in the site.

        Please provide:
          - **Request body**  data with credentials for activation

        Returns:
          - **200**: Success response with the data.
          - **400**: Error: Invalid data provided.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.auth_service.confirm_email(body=body)
        return result


schema = SchemaControl(api_settings)


@api_controller(
    "/token",
    permissions=[AllowAny],
    tags=["token"],
    auth=None,
)
class CustomTokenObtainPairController(ControllerBase):
    @http_post(
        "/pair",
        response=schema.obtain_pair_schema.get_response_schema(),
        url_name="token_obtain_pair",
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
    def obtain_token(self, request: HttpRequest, user_token: schema.obtain_pair_schema):
        """
        Get user's token by provided credentials.

        Please provide:
          - **Request body**  data with credentials of user

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        user_token.check_user_authentication_rule()
        return user_token.to_response_schema()

    @http_post(
        "/refresh",
        response=schema.obtain_pair_refresh_schema.get_response_schema(),
        url_name="token_refresh",
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
    def refresh_token(
        self,
        request: HttpRequest,
        refresh_token: schema.obtain_pair_refresh_schema,
    ):
        """
        Get user's new access token by provided refresh token.

        Please provide:
          - **Request body**  provide here refresh token

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        return refresh_token.to_response_schema()

    @http_post(
        "/verify",
        response={200: Schema},
        url_name="token_verify",
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
    def verify_token(
        self,
        request: HttpRequest,
        token: schema.verify_schema,
    ):
        """
        Check if user's token is valid.

        Please provide:
          - **Request body**  provide here user's token to check it

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        return token.to_response_schema()
