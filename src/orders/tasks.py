# -*- coding: utf-8 -*-
"""
In this module described all celery task for implementing
asynchronous logic in application orders
"""
import random
from time import sleep
from celery.app import shared_task
from django.shortcuts import get_object_or_404
from src.orders.models import Order


@shared_task
def change_order_status(order_id: int) -> dict:
    """
    Change specific order's status.

    :param order_id: order's id for changing status
    """
    order = get_object_or_404(Order, id=order_id)
    sleep(30)
    if random.choice([True, True, True, False]):
        order.status = 'COMPLETED'
        msg = "ORDER COMPLETED"
    else:
        order.status = 'CANCELED'
        msg = "ORDER CANCELED"
    order.save()
    return {"message": msg}

