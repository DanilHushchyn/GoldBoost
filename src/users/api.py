# -*- coding: utf-8 -*-
"""
    Module contains class for managing users in the site
"""
from typing import List, Tuple

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra import http_get, http_post, http_patch, http_put, http_delete
from ninja_extra.controllers.base import ControllerBase, api_controller
from ninja_jwt.authentication import JWTAuth, JWTBaseAuthentication
from config import settings
from src.users.models import User
from src.users.schemas import *
from src.users.schemas import MessageOutSchema
from src.users.services.auth_service import AuthService
from src.users.services.user_service import UserService
import jwt
from jwt.exceptions import DecodeError


@api_controller("/users")
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

    @http_post("/subscribe/{email}/", response=MessageOutSchema)
    def subscribe(self, email: str):
        """
        Endpoint for subscribing by user's email.

        :param email: user's email for subscribing
        :return: message that user subscribed
        """
        result = self.user_service.subscribe(email)
        return result

    @http_patch("/my-profile/", response=UserOutSchema, auth=JWTAuth())
    def update_my_profile(self, request: HttpRequest,
                          user_body: UserInSchema):
        """

        :param request:
        :param user_body:
        :return: Updated User model instance
        """
        result = (self.user_service.
                  update_my_profile(request.user.id, user_body))
        return result

    @http_get("/my-profile/", response=UserOutSchema, auth=JWTAuth())
    def get_my_profile(self, request: HttpRequest) -> User:
        """
        Endpoint return user's personal data to cabinet.

        :param request: request
        :return: User model instance
        """
        result = self.user_service.get_my_profile(request.user.id)
        return result

    @http_post("/create-default-character/",
               response=CharacterOutSchema,
               auth=JWTAuth())
    def create_default_character(self, request: HttpRequest) -> Character:
        """
        Endpoint for creating user's characters.

        :return: default character
        """
        result = self.user_service.create_character(request.user.id)
        return result

    @http_delete("/my-character/{character_id}",
                 response=MessageOutSchema,
                 auth=JWTAuth())
    def delete_character_by_id(self,
                               character_id: int,
                               ) -> MessageOutSchema:
        """
        Endpoint for deleting user's characters.

        :param character_id: character_id
        :return: message user's character deleted
        """
        result = self.user_service.delete_character_by_id(character_id)
        return result

    @http_patch("/my-character/{character_id}",
                response=CharacterOutSchema,
                auth=JWTAuth())
    def update_character_by_id(self,
                               character_id: int,
                               character: CharacterInSchema) \
            -> Character:
        """
        Endpoint for updating user's characters.

        :param character_id:
        :param character:
        :return: updated user's characters
        """
        result = self.user_service.update_character_by_id(character_id,
                                                          character)

        return result

    @http_get("/my-characters/", response=list[CharacterOutSchema],
              auth=JWTAuth())
    def get_my_characters(self, request: HttpRequest) -> QuerySet:
        """
        Endpoint return user's characters queryset.

        :param request: HttpRequest instance
        :return: user's characters queryset
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

    @http_post("/registration/", tags=["token"],
               response=MessageOutSchema)
    def registration(self, user: RegisterSchema) -> MessageOutSchema:
        """
        Endpoint for registration new users.

        :param user: personal data of new user
        :return: message that email send
        """
        result = self.auth_service.register_user(user)
        return result

    @http_post("/google-login/", tags=["token"],
               response=MessageOutSchema)
    def google_login_by_token(self,request, token: str) -> MessageOutSchema:
        """
        Endpoint for registration new users.

        :return: message that email send
        """
        credential = request.POST.get("credential")
        identity_data = _verify_and_decode(app=self.provider.app, credential=credential)
        login = self.provider.sociallogin_from_response(request, identity_data)
        return result

    @http_post("/reset-password/", tags=["token"])
    def reset_password(self, email: str) -> MessageOutSchema:
        """
        Endpoint for reset password.
        Part 1
        :param email: email of user who want to reset password
        :return: message that email send for reset password
        """
        result = self.auth_service.reset_password(email)
        return result

    @http_post("/change-password/", tags=["token"])
    def change_password(self, uidb64: str, token: str,
                        password1: str, password2: str) \
            -> MessageOutSchema:
        """
        Endpoint for changing user's password
        :param uidb64: user id in format base64
        :param token: token for reset operation
        :param password1: new password1
        :param password2: new password2 (confirm)
        :return:
        """
        result = (self.auth_service.
                  change_password(uidb64=uidb64,
                                  token=token,
                                  password1=password1,
                                  password2=password2))
        return result

    @http_get("/confirm-email/{uidb64}/{token}/", tags=["token"])
    def confirm_email(self, uidb64: str, token: str) -> MessageOutSchema:
        """
        Endpoint for making user active in the site
        :param uidb64: user's id encoded in base64 format
        :param token: token for reset operation
        :return: message that email confirmed and user is active
        """
        result = self.auth_service.confirm_email(uidb64=uidb64, token=token)
        return result
