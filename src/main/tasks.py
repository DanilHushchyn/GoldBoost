# -*- coding: utf-8 -*-
"""
In this module described all celery task for implementing
asynchronous logic in application orders
"""
from itertools import chain

from celery.app import shared_task
from django.core.mail import send_mail
from config import settings
from src.users.models import User, Subscriber


@shared_task
def share_news(news_title: str,
               news_descr: str) -> dict:
    """
    Send letter with news to subscribers.

    :param news_title: title of news
    :param news_descr:  description of news
    """
    users = User.objects.filter(notify_me=True).values_list('email', flat=True)
    subscribers = Subscriber.objects.values_list('email', flat=True)
    # recipients = set(users + subscribers)
    recipients = set(chain(users, subscribers))
    # Send confirmation email
    send_mail(
        news_title,
        news_descr,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )
    return {"message": "News shared successfully"}
