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
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        user = get_object_or_404(User, id=user_id)
        return user

    @staticmethod
    def register_user(user: RegisterSchema) -> dict:
        if User.objects.filter(email=user.email).exists():
            raise HttpError(403, "This email already in use ☹")
        user = User.objects.create_user(email=user.email, password=user.password, notify_me=user.notify_me)
        email_verification.delay(user_id=user.id)
        return {'message': 'Please confirm your registration. We have send letter to your email'}

    @staticmethod
    def reset_password(email: str) -> dict:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise HttpError(403, "There is not user registered with that email ☹")
        reset_password_confirm.delay(user.id)

        return {'message': 'Please confirm reset password. We have send instructions to your email'}

    @staticmethod
    def change_password( uidb64: str, token: str, password1: str, password2: str) -> dict:
        # Декодирование и проверка токена
        uid = urlsafe_base64_decode(uidb64).decode()
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise HttpError(404, "User not found ☹")
        if not default_token_generator.check_token(user, token):
            raise HttpError(400, "Invalid token")
        if password1 != password2:
            raise HttpError(400, "Passwords aren't the same")

        # Изменение пароля пользователя
        user.set_password(password1)
        user.save()

        # Удаление токена сброса пароля
        PasswordResetToken.objects.filter(user=user).delete()

        return {"detail": "Password reset successfully."}


    @staticmethod
    def confirm_email(uidb64: str, token: str) -> dict:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return {"message": "Email confirmed successfully"}
        else:
            return {"message": "Invalid confirmation link"}
