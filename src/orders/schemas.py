# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "orders"
implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import ModelSchema, Schema
from pydantic.types import conlist

from config.settings import ABSOLUTE_URL
from src.orders.models import Attribute, Cart, CartItem
from src.products.models import Product


class AttributeSchema(ModelSchema):
    """
    Pydantic schema for Attribute.
    Purpose of this schema to return
    related attributes for OrderItem model instance
    """

    title: str
    subtitle: str
    price: float

    @staticmethod
    def resolve_title(obj: Attribute):
        return obj.sub_filter.filter.title

    @staticmethod
    def resolve_price(obj: Attribute):
        return obj.sub_filter.price

    @staticmethod
    def resolve_subtitle(obj: Attribute):
        return obj.sub_filter.title

    class Meta:
        model = Attribute
        exclude = ("id", "sub_filter", "cart_item")


# class CartItemSchema(ModelSchema):
#     """
#     Pydantic schema for OrderItem.
#
#     Purpose of this schema to return info about
#     order item in cart
#     """
#     title: str
#     subtitle: str
#     game_logo: str
#     game_logo_alt: str
#     card_img: str
#     card_img_alt: str
#     attributes: List[AttributeSchema]
#     price: float
#     bonus_points: int
#
#     @staticmethod
#     def resolve_title(obj):
#         return obj.product.title
#
#     @staticmethod
#     def resolve_subtitle(obj):
#         return obj.product.subtitle
#
#     @staticmethod
#     def resolve_game_logo(obj):
#         return (f"{ABSOLUTE_URL}"
#                 f"{obj.product.catalog_page.game.logo_product.url}")
#
#     @staticmethod
#     def resolve_game_logo_alt(obj):
#         return obj.product.catalog_page.game.logo_product_alt
#
#     @staticmethod
#     def resolve_card_img(obj):
#         return (f"{ABSOLUTE_URL}"
#                 f"{obj.product.catalog_page.game.logo_product.url}")
#
#     @staticmethod
#     def resolve_card_img_alt(obj):
#         return obj.product.card_img_alt
#
#     @staticmethod
#     def resolve_bonus_points(obj):
#         return obj.product.bonus_points * obj.quantity
#
#     class Meta:
#         model = CartItem
#         fields = "__all__"
#         exclude = ("cart",)


class CartItemProductSchema(ModelSchema):
    """
    Pydantic schema for Product.

    Purpose of this schema to return info about product
    for product element in carousel in client side
    """

    game_logo: str
    game_logo_alt: str
    sale_price: float | None
    sale_percent: float | None
    price: float | None
    sale_active: bool
    sale_period: str | None
    attributes: List[AttributeSchema] = []

    @staticmethod
    def resolve_game_logo(obj: Product):
        return f"{ABSOLUTE_URL}{obj.catalog_page.game.logo_product.url}"

    @staticmethod
    def resolve_game_logo_alt(obj: Product):
        return obj.catalog_page.game.logo_product_alt

    @staticmethod
    def resolve_card_img(obj):
        return ABSOLUTE_URL + obj.card_img.url

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "subtitle",
            "price",
            "card_img",
            "card_img_alt",
        ]


class CartItemSchema(ModelSchema):
    """
    Pydantic schema for OrderItem.

    Purpose of this schema to return info about
    order item in cart
    """

    items: List[CartItemProductSchema]
    cost: float
    cost_with_sale: float | None
    sale_active: bool
    sale_percent: int | None
    bonus_points: int

    @staticmethod
    def resolve_items(obj: CartItem):
        if obj.product:
            obj.product.attributes = obj.attributes
            return [obj.product]
        return obj.freqbot.products

    class Meta:
        model = CartItem
        fields = "__all__"
        exclude = ("cart", "product", "freqbot", "date_created")


class CartOutSchema(Schema):
    """
    Pydantic schema for Cart in the site.

    Purpose of this schema to return info
    all products added ti cart by user
    """

    items: List[CartItemSchema]
    total_bonuses: int
    total_price: float
    count: int
    next: bool
    previous: bool


class CreateOrderInSchema(Schema):
    """
    Pydantic schema for CartItems.

    Purpose of this schema to send
    ids of cart items to endpoint for creating order
    """

    items: conlist(int, min_length=1)
    promo_code: str | None = None
