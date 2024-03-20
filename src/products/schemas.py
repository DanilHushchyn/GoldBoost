# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "products".

Implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import ModelSchema, Schema
from pydantic.types import conint

from config.settings import ABSOLUTE_URL
from src.products.models import Filter, Product, SubFilter, Tag, ProductTabs


class TagOutSchema(ModelSchema):
    """
    Pydantic schema for Tag.

    Purpose of this schema to return info about tag(name,color)
    to client side
    """

    class Meta:
        model = Tag
        fields = "__all__"
        exclude = ("id",)


class ProductSchema(ModelSchema):
    """
    Pydantic schema for Product.

    Purpose of this schema to return info about product
    for product element in carousel in client side
    """

    tag: TagOutSchema | None
    # первый вариант как вернуть картинку игры
    # game_logo: str = Field(None, alias="catalog_page.game.logo_product")
    price_from: float | None
    price_to: float | None
    sale_price_from: float | None
    sale_price_to: float | None
    sale_price: float | None
    sale_period: str | None
    sale_active: bool

    @staticmethod
    def resolve_game_logo(obj):
        return f"{ABSOLUTE_URL}{obj.catalog_page.game.logo_product.url}"

    @staticmethod
    def resolve_card_img(obj):
        return ABSOLUTE_URL + obj.card_img.url

    @staticmethod
    def resolve_image(obj):
        return ABSOLUTE_URL + obj.image.url

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("bought_count",)


class ProductsSectionSchema(Schema):
    items: List[ProductSchema]
    count: int


class HotSectionSchema(Schema):
    """
    Pydantic schema for Section "Hot Carousel".

    Purpose of this schema to return info about product
    which filtered be tag hot
    """

    items: List[ProductSchema]
    count: int
    next: bool
    previous: bool


class BestSellersSchema(Schema):
    """
    Pydantic schema for BestSellers.

    Purpose of this schema to return info about product
    which ordered be parameter bought_count
    """

    items: List[ProductSchema]
    count: int
    next: bool
    previous: bool


class SubFilterItemSchema(ModelSchema):
    """
    Pydantic schema for SubFilter.

    Purpose of this schema to return
    Subfilter model instance
    """

    class Meta:
        model = SubFilter
        fields = "__all__"
        exclude = ("filter", 'order')


class FilterItemSchema(ModelSchema):
    """
    Pydantic schema for Filter.

    Purpose of this schema to return
    Filter model instance and related SubFilter
    queryset
    """

    subfilters: List[SubFilterItemSchema]

    class Meta:
        model = Filter
        fields = "__all__"
        exclude = ("id", "product", 'order')


class ProductTabSchema(ModelSchema):
    """
    Pydantic schema for ProductTabs.

    Purpose of this schema to return
    Filter model instance and related ProductTabs
    queryset
    """

    class Meta:
        model = ProductTabs
        fields = "__all__"
        exclude = ['content', 'product', 'order']


class ProductCardSchema(ModelSchema):
    """
    Pydantic schema for Product.

    Purpose of this schema to return
    Product model instance and related
    Filter queryset
    """

    filters: List[FilterItemSchema] | None
    price_from: float | None
    price_to: float | None
    sale_price_from: float | None
    sale_price_to: float | None
    sale_price: float | None
    sale_period: str | None
    sale_active: bool
    tabs: List[ProductTabSchema]

    @staticmethod
    def resolve_image(obj):
        return ABSOLUTE_URL + obj.image.url

    @staticmethod
    def resolve_card_img(obj):
        return ABSOLUTE_URL + obj.card_img.url

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("bought_count", "tag")


class GameCarouselsMainSchema(Schema):
    """
    Pydantic schema for Game Carousel.

    Purpose of this schema to return
    paginated queryset of products
    """

    items: List[ProductSchema]
    count: int
    next: bool
    previous: bool


class TabContentSchema(ModelSchema):
    """
    Pydantic schema for model ProductTabs.

    Purpose of this schema to return
    content for tab to client side
    """

    class Meta:
        model = ProductTabs
        fields = ["content"]


class AddToCartSchema(Schema):
    """
    Pydantic schema for adding products to cart.

    Please provide:
      - **attributes**: array of id of filters related to product
      if needed(only for product with range price)
      - **quantity**: number of products we want to add to cart
    """
    attributes: list[int] = []
    quantity: conint(gt=0)


class ProductSearchSchema(ModelSchema):
    class Meta:
        model = Product
        fields = ["id", 'title']
