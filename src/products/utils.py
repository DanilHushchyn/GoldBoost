# -*- coding: utf-8 -*-
"""
This file contains most frequently used methods for
app product
    Methods:
        paginate - helps to paginate any queryset
        get_timestamp_path - helps to make unique name
        for just uploaded file to the system in media directory
"""
import datetime
from os.path import splitext

from django.core.paginator import EmptyPage, Paginator
from django.db.models.query import QuerySet


def paginate(page: int, items: QuerySet, page_size: int) -> dict:
    """
    Returns paginated queryset by pages of any Model in our project
    :param page: the page number we want to get
    :param items: queryset of models instances which have to paginated
    :param page_size: length of queryset per page
    :return: dict which contains parameters for pagination
    :rtype: dict
    """
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
    Make unique naming of files in directory media
    :param instance: model instance which just created
    :param filename: name of uploaded file to ImageField
    :return: unique file name
    """
    return "%s%s" % (
        datetime.datetime.now().timestamp(),
        splitext(filename)[1],
    )
