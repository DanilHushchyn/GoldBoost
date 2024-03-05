from ninja_extra import Router, http_get, http_post, http_generic, http_delete
from ninja_extra.controllers.base import ControllerBase, api_controller
from src.users.schemas import UserOutSchema, RegisterSchema, MessageOutSchema
from src.users.services.auth_service import AuthService
from src.users.services.user_service import UserService


@api_controller('/users')
class UsersController(ControllerBase):
    """
    A controller class for managing users and cabinet(subdomain's private part of site).
    """

    def __init__(self, user_service: UserService):
        """
        Use this method to inject "services" to endpoints of AuthController
        :param user_service: variable for managing user's data in system
        """
        self.user_service = user_service

    @http_get('/{user_id}/', response=UserOutSchema)
    def get_user_id(self, user_id: int):
        result = self.user_service.get_user_by_id(user_id)
        return result


@api_controller('/auth', tags=['token'])
class AuthController(ControllerBase):
    """
    A controller class for managing access control system on site.
    This class provides endpoints for registration,login,reset password and so on
    """

    def __init__(self, auth_service: AuthService):
        """
        Use this method to inject "services" to endpoints of AuthController
        :param auth_service: variable for managing access control system
        """
        self.auth_service = auth_service

    @http_post('/registration/', tags=['token'], response=MessageOutSchema)
    def registration(self, user: RegisterSchema) -> MessageOutSchema:
        result = self.auth_service.register_user(user)
        return result

    @http_post('/reset-password/', tags=['token'])
    def reset_password(self, email: str) -> MessageOutSchema:
        result = self.auth_service.reset_password(email)
        return result

    @http_post('/change-password/', tags=['token'])
    def change_password(self, uidb64: str, token: str, password1: str, password2: str) -> MessageOutSchema:
        result = self.auth_service.change_password(uidb64=uidb64, token=token, password1=password1, password2=password2)
        return result

    @http_get("/confirm-email/{uidb64}/{token}/", tags=['token'])
    def confirm_email(self, uidb64: str, token: str) -> MessageOutSchema:
        result = self.auth_service.confirm_email(uidb64=uidb64, token=token)
        return result
