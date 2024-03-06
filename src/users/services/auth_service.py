# -*- coding: utf-8 -*-
from http.client import HTTPException

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ninja.errors import HttpError

from src.users.models import PasswordResetToken, User
from src.users.schemas import MessageOutSchema, RegisterSchema
from src.users.tasks import email_verification, reset_password_confirm


class AuthService:
    """
    A service class for managing access control system on site.
    This class provides endpoints for registration, login, reset password and so on.
    """

    @staticmethod
    def register_user(user: RegisterSchema) -> MessageOutSchema:
        """
        Part 1 of register new users on the site
        :param user: stores a set of user data for registration
        :return: str message that registration successful
        """
        if User.objects.filter(email=user.email).exists():
            raise HttpError(403, "This email already in use ☹")
        user = User.objects.create_user(email=user.email, password=user.password, notify_me=user.notify_me)
        email_verification.delay(user_id=user.id)
        return MessageOutSchema(message="Please confirm your registration. We have send letter to your email")

    @staticmethod
    def confirm_email(uidb64: str, token: str) -> MessageOutSchema:
        """
        Part 2 of register new users on the site
        Method check that email exists in system and
        send letter with instructions for reset password Part 2
        :param token: is used for validation registration operation
               and identify user
        :param uidb64: store user id in base64 format
        :return: str message that email confirmed and user active
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return MessageOutSchema(message="Email confirmed successfully")
        else:
            raise HttpError(400, "Invalid confirmation link")

    @staticmethod
    def reset_password(email: str) -> MessageOutSchema:
        """
        Part 1 of reset user's password
        method check that email exists in system and
        send letter with instructions for reset password Part 2
        :param email: user's email helps to find him
        :return: str message that reset started
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise HttpError(403, "There is not user registered with that email ☹")
        reset_password_confirm.delay(user.id)

        return MessageOutSchema(message="Please confirm reset password. We have send instructions to your email")

    @staticmethod
    def change_password(uidb64: str, token: str, password1: str, password2: str) -> MessageOutSchema:
        """
        Part 2 of reset user's password
        method decodes token and
        send letter with instructions for reset password Part 2
        :param password1: new password
        :param password2: confirm new password
        :param token: is used for validation reset password operation
               and identify user
        :param uidb64: store user id in base64 format
        :return: str message that reset started
        """
        # Decode and check token
        uid = urlsafe_base64_decode(uidb64).decode()
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise HttpError(404, "User not found ☹")
        if not default_token_generator.check_token(user, token):
            raise HttpError(400, "Invalid token")
        if password1 != password2:
            raise HttpError(400, "Passwords aren't the same")

        # Change user's password
        user.set_password(password1)
        user.save()

        # Delete user's token for password reset
        PasswordResetToken.objects.filter(user=user).delete()

        return MessageOutSchema(message="Password reset successfully.")
