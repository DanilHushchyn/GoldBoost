# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "products"
implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import Field, ModelSchema, Schema
from pydantic.types import conint

from config.settings import ABSOLUTE_URL
from src.games.models import Tab, TabItem
from src.products.models import Filter, Product, SubFilter, Tag


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
        exclude = ("bought_count", "tab")


class ProductsSectionSchema(Schema):
    items: List[ProductSchema]
    count: int


class HotSectionSchema(Schema):
    """
    Pydantic schema for Section "Hot Carousel" .
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


class TabItemSchema(ModelSchema):
    """
    Pydantic schema for TabItem
    Purpose of this schema to return id
    for future requests from client side
    """

    class Meta:
        model = TabItem
        fields = "__all__"
        exclude = ("tab", "content", "order")


class TabSchema(ModelSchema):
    """
    Pydantic schema for Tab
    Purpose of this schema to return
    Tab model instance and related TabItem
    queryset
    """

    tab_items: List[TabItemSchema] | None

    class Meta:
        model = Tab
        fields = "__all__"
        exclude = ("id",)


class SubFilterItemSchema(ModelSchema):
    """
    Pydantic schema for SubFilter
    Purpose of this schema to return
    Subfilter model instance
    """

    class Meta:
        model = SubFilter
        fields = "__all__"
        exclude = ("filter",)


class FilterItemSchema(ModelSchema):
    """
    Pydantic schema for Filter
    Purpose of this schema to return
    Filter model instance and related SubFilter
    queryset
    """

    subfilters: List[SubFilterItemSchema]

    class Meta:
        model = Filter
        fields = "__all__"
        exclude = ("id", "product")


class ProductCardSchema(ModelSchema):
    """
    Pydantic schema for Product
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
    Pydantic schema for Game Carousel
    Purpose of this schema to return
    paginated queryset of products
    """

    items: List[ProductSchema]
    count: int
    next: bool
    previous: bool


class TabContentSchema(ModelSchema):
    """
    Pydantic schema for model TabItem
    Purpose of this schema to return
    content for tab to client side
    """

    class Meta:
        model = TabItem
        exclude = ["id", "title", "tab", "order"]


class AddToCartSchema(Schema):
    """
    Pydantic schema for adding products to cart
    Purpose of this schema, from
    Product model instance create OrderItem model instance
    """
    attributes: list = []
    quantity: conint(gt=0)
