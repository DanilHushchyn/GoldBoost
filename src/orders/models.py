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
from django.utils.translation import gettext_lazy as _

from src.products.models import FreqBought, Product, SubFilter
from src.products.utils import make_sale
from src.users.models import User


# Create your models here.
class Order(models.Model):
    """
    Model is storing order of users in the site
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Key to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    number = models.PositiveBigIntegerField(null=True, unique=True)
    # Status Choices
    ORDER_STATUS_CHOICES = (
        ("IN PROGRESS", _("IN PROGRESS")),
        ("CANCELED", _("CANCELED")),
        ("COMPLETED", _("COMPLETED")),
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="CANCELED")
    date_created = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()

    class Meta:
        ordering = ["-date_created"]
        verbose_name = "Orders"
        verbose_name_plural = "Orders"
        db_table = "orders"


class Cart(models.Model):
    """
    Model is order items before buying them by users
    """

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=500, null=True, unique=True)

    class Meta:
        db_table = "carts"


class CartItem(models.Model):
    """
    Model represents cart's items in the site
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="cart_items")
    freqbot = models.ForeignKey(FreqBought, on_delete=models.CASCADE, null=True, related_name="cart_items")
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE, related_name="items")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def price_for_product(self, product: Product):
        total = product.price
        for attr in self.attributes.all():
            total = total + attr.sub_filter.price
        # if product.sale_active():
        #     if product.price_type == "fixed":
        #         total = product.sale_price()
        #     else:
        #         total = make_sale(total, product.sale_percent)
        return total * self.quantity

    def price_for_product_with_sale(self, product: Product):
        total = product.price
        for attr in self.attributes.all():
            total = total + attr.sub_filter.price
        if product.sale_active():
            if product.price_type == "fixed":
                total = product.sale_price()
            else:
                total = make_sale(total, product.sale_percent)
        return total * self.quantity

    def price(self):
        if self.product:
            return self.price_for_product_with_sale(self.product)
        else:
            total = 0
            for product in self.freqbot.products.all():
                total = total + self.price_for_product_with_sale(product)
            return make_sale(total, self.freqbot.discount)

    def cost_with_sale(self):
        return self.price()

    def sale_active(self):
        if self.freqbot:
            return True
        if self.product.sale_active():
            return True
        return False

    def sale_percent(self):
        if self.freqbot:
            return self.freqbot.discount
        if self.sale_active():
            return self.product.sale_percent
        return 0

    def cost(self):
        if self.product:
            return self.price_for_product(self.product)
        else:
            total = 0
            for product in self.freqbot.products.all():
                total = total + self.price_for_product(product)
            return total

    def bonus_points(self):
        if self.product:
            return self.product.bonus_points * self.quantity
        else:
            total = 0
            for product in self.freqbot.products.all():
                total = total + product.bonus_points
            return total

    class Meta:
        ordering = ["-date_created"]
        db_table = "cart_items"


class Attribute(models.Model):
    """
    Model is storing additional attributes.

    for ordered product
    """

    sub_filter = models.ForeignKey(SubFilter, on_delete=models.CASCADE, null=True)
    cart_item = models.ForeignKey("CartItem", on_delete=models.CASCADE, null=True, related_name="attributes")

    class Meta:
        db_table = "attributes"
