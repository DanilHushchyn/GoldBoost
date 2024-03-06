# -*- coding: utf-8 -*-
from http.client import HTTPException

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ninja.errors import HttpError

from src.users.models import PasswordResetToken, User
from src.users.schemas import RegisterSchema
from src.users.tasks import email_verification, reset_password_confirm


class UserService:
    """
    A service class for managing users.
    """

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        user = get_object_or_404(User, id=user_id)
        return user
