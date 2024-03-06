# -*- coding: utf-8 -*-
"""
    In this module described models for application orders
    Their purpose is storing data for orders and related to orders data
    Models:
       Order
       Cart
       OrderItem
       Attribute
"""
# -*- coding: utf-8 -*-
from django.db import models

from src.products.models import Product, SubFilter
from src.users.models import User


# Create your models here.
class Order(models.Model):
    # Foreign Key to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Status Choices
    ORDER_STATUS_CHOICES = (
        ("in progress", "IN PROGRESS"),
        ("canceled", "CANCELED"),
        ("completed", "COMPLETED"),
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    date_created = models.DateField()
    order_number = models.UUIDField(unique=True)
    total_price = models.FloatField()

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Orders"


class Cart(models.Model):
    # OneToOneField to User model
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # Session Key
    session_key = models.CharField(max_length=255)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
    )
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)


class Attribute(models.Model):
    # Fields
    sub_filter = models.ForeignKey(SubFilter, on_delete=models.CASCADE, null=True)
    order_item = models.ForeignKey("OrderItem", on_delete=models.CASCADE, null=True)
