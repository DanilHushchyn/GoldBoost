from http.client import HTTPException

from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from src.users.models import User, PasswordResetToken
from src.users.schemas import RegisterSchema
from src.users.tasks import email_verification, reset_password_confirm
from django.urls import reverse


class UserService:
    """
    A service class for managing users.
    """
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        user = get_object_or_404(User, id=user_id)
        return user

