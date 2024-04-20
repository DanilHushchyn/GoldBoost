# -*- coding: utf-8 -*-
"""
    Module contains class for managing access control system in the site.

"""
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialLogin
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from ninja_jwt.tokens import RefreshToken, AccessToken

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from ninja.errors import HttpError
from loguru import logger
from src.users.models import PasswordResetToken, Subscriber, User
from src.users.schemas import ChangePasswordSchema, ConfirmationSchema, EmailSchema, MessageOutSchema, RegisterSchema
from src.users.tasks import email_verification, reset_password_confirm


class AuthService:
    """
    A service class for managing access control system on site.

    This class provides endpoints for registration, login,
    reset password and so on.
    """

    @staticmethod
    def register_user(user_body: RegisterSchema) -> MessageOutSchema:
        """
        Part 1 of register new users on the site.

        :param user_body: stores a set of user data for registration
        :return: str message that registration successful
        """
        if User.objects.filter(email=user_body.email).exists():
            raise HttpError(409, _("This email already in use"))
        user = User.objects.create_user(
            email=user_body.email, password=user_body.password, notify_me=user_body.notify_me
        )
        subscribed = Subscriber.objects.filter(email=user.email).exists()
        if subscribed:
            subscriber = Subscriber.objects.get(email=user.email)
            subscriber.delete()
            user.subscribe_sale_active = True

        if user.notify_me is True:
            user.subscribe_sale_active = True
        user.save()
        token = default_token_generator.make_token(user)
        email_verification.delay(user_id=user.id, token=token)
        return MessageOutSchema(
            message=_("Please confirm " "your registration. " "We have send letter " "to your email")
        )

    @staticmethod
    def social_login(
            request: HttpRequest,
            app: SocialApp,
            adapter: OAuth2Adapter,
            access_token: str,
            response=None,
            connect=True,
    ):
        """
        Uses allauth to complete a social login
        If connect is True, then a new social account will be connected to an existing user
        Otherwise, raises an error if the email already exists
        If the email does not exist, then a new user will be created
        Apparently, its not very secure to use connect = True for lesser known social apps
        """
        if not isinstance(request, HttpRequest):
            request = request._request
        token = adapter.parse_token({"access_token": access_token})
        token.app = app
        try:
            response = response or {}
            login: SocialLogin = adapter.complete_login(request, app, token, response)
            login.token = token
            complete_social_login(request, login)
        except Exception as e:
            return 400, {"detail": f"Could not complete social login: {e}"}
        if not login.is_existing:
            user = User.objects.filter(email=login.user.email).first()
            if user:
                if connect:
                    login.connect(request, user)
                else:
                    return 400, {"detail": ["Email already exists"]}
            else:
                login.lookup()
                login.save(request)
        try:
            user = User.objects.get(email=login.account.extra_data['email'])
        except Exception as e:
            return 400, {"detail": f"Could not complete social login: {e}"}

        refresh = RefreshToken.for_user(user)
        return refresh

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
        if user is not None and default_token_generator.check_token(user, body.token):
            if user.is_active:
                return MessageOutSchema(message=_("Email has already been confirmed"))
            user.is_active = True
            user.save()
            return MessageOutSchema(message=_("Email has been confirmed successfully"))
        else:
            raise HttpError(400, _("Invalid link"))

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
            raise HttpError(403, _("There is not user registered" " with that email"))
        token = default_token_generator.make_token(user)
        reset_password_confirm.delay(user.id, token)
        return MessageOutSchema(
            message=_("Please confirm " "reset password." " We have send " "instructions to your email")
        )

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
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise HttpError(400, _("Invalid link"))
        if not default_token_generator.check_token(user, body.token):
            raise HttpError(400, _("Invalid link"))
        if body.password1 != body.password2:
            raise HttpError(403, _("Passwords aren't the same"))

        # Change user's password
        user.set_password(body.password1)
        user.save()

        # Delete user's token for password reset
        PasswordResetToken.objects.filter(user=user).delete()
        return MessageOutSchema(message=_("Password reset successfully."))

    @staticmethod
    def check_change_password(body: ConfirmationSchema) -> MessageOutSchema:
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
            raise HttpError(400, _("Invalid link"))
        if not default_token_generator.check_token(user, body.token):
            raise HttpError(400, _("Invalid link"))

        return MessageOutSchema(message=_("Promo code is valid."))
