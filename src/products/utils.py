# -*- coding: utf-8 -*-
"""
This file contains most frequently used methods for app product.

    Methods:
        paginate - helps to paginate any queryset
        get_timestamp_path - helps to make unique name
        for just uploaded file to the system in media directory
"""
from datetime import datetime, timedelta
from os.path import splitext

import jwt
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from jwt.exceptions import PyJWTError
from ninja.errors import HttpError

from config import settings


def paginate(page: int, items: QuerySet, page_size: int) -> dict:
    """
    Returns paginated queryset by pages of any Model in our project.

    :param page: the page number we want to get
    :param items: queryset of models instances which have to paginated
    :param page_size: length of queryset per page
    :return: dict which contains parameters for pagination
    :rtype: dict
    """
    if page_size < 1:
        raise HttpError(422, "page_size query parameter must be more than 1 ☹")
    paginator = Paginator(items, per_page=page_size)
    try:
        paginated_items = paginator.page(page)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return {
        "items": paginated_items.object_list,
        "count": paginator.num_pages,
        "next": paginated_items.has_next(),
        "previous": paginated_items.has_previous(),
    }


def get_timestamp_path(instance: object, filename) -> str:
    """
    Make unique naming of files in directory media.

    :param instance: model instance which just created
    :param filename: name of uploaded file to ImageField
    :return: unique file name
    """
    return "%s%s" % (
        datetime.now().timestamp(),
        splitext(filename)[1],
    )


def get_current_user(token: str):
    """
    Check auth user.

    """
    try:
        code, token = token.split(" ")
        if code != "Bearer":
            raise ValueError
        payload = jwt.decode(token, settings.NINJA_JWT["SIGNING_KEY"], algorithms=[settings.NINJA_JWT["ALGORITHM"]])
    except (PyJWTError, ValueError):
        return False

    token_exp = datetime.fromtimestamp(int(payload["exp"]))
    if token_exp < datetime.utcnow():
        return False

    user = get_object_or_404(get_user_model(), id=payload["user_id"])
    return user

# def get_auth(request:HttpRequest):


def make_sale(price: float, sale: int):
    sale = (price * sale) / 100
    return price - sale
