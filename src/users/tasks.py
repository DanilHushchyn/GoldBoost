from celery.app import shared_task
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from config import settings
from config.celery import app
from src.users.models import User, PasswordResetToken


@shared_task
def email_verification(user_id: int):
    user = User.objects.get(id=user_id)
    # Send confirmation email
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirmation_url = f"{settings.FRONTEND_URL}/confirm-email/{uid}/{token}"
    send_mail(
        "Confirm Your Email for site GoldBoost",
        f"Click the link to confirm your email: {confirmation_url}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return {"message": "Confirmation email sent"}


@shared_task
def reset_password_confirm(user_id: int):
    user = User.objects.get(id=user_id)

    # Генерация токена сброса пароля
    token = default_token_generator.make_token(user)
    PasswordResetToken.objects.create(user=user, token=token)

    # Создание ссылки для подтверждения сброса пароля
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{settings.FRONTEND_URL}/change-password/{uid}/{token}"

    # Отправка электронного письма с ссылкой для подтверждения сброса пароля
    send_mail(
        'Password reset',
        f'Click the following link to reset your password: {reset_url}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return {"message": "Reset password confirmation sent to email"}