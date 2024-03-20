# -*- coding: utf-8 -*-
"""
    Module contains class for managing access control system in the site.

"""
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from ninja.errors import HttpError
from src.users.models import PasswordResetToken, User
from src.users.schemas import MessageOutSchema, RegisterSchema, ConfirmationSchema, ChangePasswordSchema, EmailSchema
from src.users.tasks import email_verification, reset_password_confirm


class AuthService:
    """
    A service class for managing access control system on site.

    This class provides endpoints for registration, login,
    reset password and so on.
    """

    @staticmethod
    def register_user(user: RegisterSchema) -> MessageOutSchema:
        """
        Part 1 of register new users on the site.

        :param user: stores a set of user data for registration
        :return: str message that registration successful
        """
        if User.objects.filter(email=user.email).exists():
            raise HttpError(409, "This email already in use ☹")
        user = User.objects.create_user(email=user.email,
                                        password=user.password,
                                        notify_me=user.notify_me)
        token = default_token_generator.make_token(user)

        email_verification.delay(user_id=user.id, token=token)
        return MessageOutSchema(message="Please confirm "
                                        "your registration. "
                                        "We have send letter "
                                        "to your email")

    @staticmethod
    def confirm_email(body: ConfirmationSchema) -> MessageOutSchema:
        """
        Part 2 of register new users on the site.

        Method check that email exists in system and
        send letter with instructions for reset password Part 2
        :param body: token and uidb64 for checking
        :return: str message that email confirmed and user active
        """
        try:
            uid = force_str(urlsafe_base64_decode(body.uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (user is not None and
                default_token_generator.check_token(user, body.token)):
            if user.is_active:
                return MessageOutSchema(message="Email already confirmed")
            user.is_active = True
            user.save()
            return MessageOutSchema(message="Email confirmed successfully")
        else:
            raise HttpError(400, "Invalid link ☹")

    @staticmethod
    def reset_password(body: EmailSchema) -> MessageOutSchema:
        """
        Part 1 of reset user's password.

        Method check that email exists in system and
        send letter with instructions for reset password Part 2
        :param body: user's email helps to find him
        :return: str message that reset started
        """
        try:
            user = User.objects.get(email=body.email)
        except User.DoesNotExist:
            raise HttpError(403,
                            "There is not user registered"
                            " with that email ☹")
        token = default_token_generator.make_token(user)
        reset_password_confirm.delay(user.id, token)
        return MessageOutSchema(message="Please confirm "
                                        "reset password."
                                        " We have send "
                                        "instructions to your email")

    @staticmethod
    def change_password(body: ChangePasswordSchema) -> MessageOutSchema:
        """
        Part 2 of reset user's password.

        method decodes token and
        send letter with instructions for reset password Part 2
        :param body,
        body.password1: new password
        body.password2: confirm new password
        body.token: is used for validation reset password operation
               and identify user
        body.uidb64: store user id in base64 format
        :return: str message that reset started
        """
        # Decode and check token
        try:
            uid = urlsafe_base64_decode(body.uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,User.DoesNotExist):
            raise HttpError(400, "Invalid link ☹")
        if not default_token_generator.check_token(user, body.token):
            raise HttpError(400, "Invalid link ☹")
        if body.password1 != body.password2:
            raise HttpError(403, "Passwords aren't the same ☹")

        # Change user's password
        user.set_password(body.password1)
        user.save()

        # Delete user's token for password reset
        PasswordResetToken.objects.filter(user=user).delete()
        return MessageOutSchema(message="Password reset successfully.")

    @staticmethod
    def check_change_password(body: ConfirmationSchema) \
            -> MessageOutSchema:
        """
        Check tokens and uidb64 if is valid.

        :param body: token and uidb64 for checking
        :return: str message that checked
        """
        # Decode and check token
        try:
            uid = urlsafe_base64_decode(body.uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise HttpError(400, "Invalid link ☹")
        if not default_token_generator.check_token(user, body.token):
            raise HttpError(400, "Invalid link ☹")

        return MessageOutSchema(message="Data is valid.")
