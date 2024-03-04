import uuid
from django.http import HttpRequest
from ninja.errors import HttpError
from ninja_extra import Router, http_get, http_post, http_generic, http_delete
from ninja_extra.controllers.base import ControllerBase, api_controller
from ninja import ModelSchema
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from src.users.models import User, PasswordResetToken
from src.users.schemas import UserOutSchema, SubscribeInSchema, RegisterSchema
from src.users.services.user_service import UserService

from src.users.tasks import email_verification, reset_password_confirm


@api_controller('/users')
class UsersController(ControllerBase):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @http_post('/registration/', tags=['token'])
    def registration(self, user: RegisterSchema):
        result = self.user_service.register_user(user)
        return result

    @http_post('/reset-password/', tags=['token'])
    def reset_password(self, email: str):
        result = self.user_service.reset_password(email)
        return result

    @http_post('/change-password/', tags=['token'])
    def change_password(self, uidb64: str, token: str, password1: str, password2: str):
        result = self.user_service.change_password(uidb64=uidb64, token=token, password1=password1, password2=password2)
        return result

    @http_get('/{user_id}/', response=UserOutSchema)
    def get_user_id(self, user_id: int):
        result = self.user_service.get_user_by_id(user_id)
        return result

    @http_get("/confirm-email/{uidb64}/{token}/", tags=['token'])
    def confirm_email(self, uidb64: str, token: str):
        result = self.user_service.confirm_email(uidb64=uidb64, token=token)
        return result
