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
import uuid

# -*- coding: utf-8 -*-
from django.db import models

from src.products.models import Product, SubFilter
from src.users.models import User


# Create your models here.
class Order(models.Model):
    """
    Model is storing order of users in the site
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)

    # Foreign Key to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Status Choices
    ORDER_STATUS_CHOICES = (
        ("in progress", "IN PROGRESS"),
        ("canceled", "CANCELED"),
        ("completed", "COMPLETED"),
    )
    status = models.CharField(max_length=20,
                              choices=ORDER_STATUS_CHOICES,
                              default='canceled')
    date_created = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Orders"
        verbose_name_plural = "Orders"
        db_table = 'orders'


class Cart(models.Model):
    """
    Model is order items before buying them by users
    """

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'carts'


class CartItem(models.Model):
    """
    Model represents cart's items in the site
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
    )
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, null=True,
                             on_delete=models.CASCADE,
                             related_name='items')

    def price(self):
        total = self.product.price
        if self.product.sale_active():
            total = self.product.sale_price()
        for attr in self.attributes.all():
            total = total + attr.sub_filter.price
        return total * self.quantity

    class Meta:
        db_table = 'cart_items'


class Attribute(models.Model):
    """
    Model is storing additional attributes
    for ordered product
    """

    sub_filter = models.ForeignKey(SubFilter,
                                   on_delete=models.CASCADE,
                                   null=True)
    cart_item = models.ForeignKey("CartItem",
                                  on_delete=models.CASCADE,
                                  null=True, related_name='attributes')

    class Meta:
        db_table = 'attributes'
