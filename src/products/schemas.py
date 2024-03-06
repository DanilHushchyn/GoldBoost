# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "products"
implement logic for encoding and decoding data into python
object and json
"""
from typing import List
from ninja import Field, ModelSchema, Schema
from src.games.models import Tab, TabItem
from src.products.models import Filter, Product, SubFilter, Tag


class TagOutSchema(ModelSchema):
    """

    """
    class Meta:
        model = Tag
        fields = "__all__"
        exclude = ("id",)


class ProductSchema(ModelSchema):
    tag: TagOutSchema | None
    # первый вариант как вернуть картинку игры
    game_logo: str = Field(None, alias="catalog_page.game.logo_product")
    price_from: float | None
    price_to: float | None
    sale_price_from: float | None
    sale_price_to: float | None
    sale_price: float | None
    sale_period: str | None
    sale_active: bool

    # @staticmethod
    # def resolve_game_logo(obj):
    # второй вариант как вернуть картинку игры
    #     return f"{obj.catalog_page.game.logo_product.url}"
    #
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("bought_count", "tab")


class ProductsSectionSchema(Schema):
    items: List[ProductSchema]
    count: int


class HotSectionSchema(Schema):
    items: List[ProductSchema]
    count: int
    next: bool
    previous: bool


class BestSellersSchema(Schema):
    items: List[ProductSchema]
    count: int
    next: bool
    previous: bool


class TabItemSchema(ModelSchema):
    class Meta:
        model = TabItem
        fields = "__all__"
        exclude = ("tab", "content", "order")


class TabSchema(ModelSchema):
    tab_items: List[TabItemSchema] | None

    class Meta:
        model = Tab
        fields = "__all__"
        exclude = ("id",)


class SubFilterItemSchema(ModelSchema):
    class Meta:
        model = SubFilter
        fields = "__all__"
        exclude = ("filter",)


class FilterItemSchema(ModelSchema):
    subfilters: List[SubFilterItemSchema]

    class Meta:
        model = Filter
        fields = "__all__"
        exclude = ("id", "product")


class ProductCardSchema(ModelSchema):
    filters: List[FilterItemSchema] | None
    price_from: float | None
    price_to: float | None
    sale_price_from: float | None
    sale_price_to: float | None
    sale_price: float | None
    sale_period: str | None
    sale_active: bool

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("bought_count", "tag")


class ProductCountPriceIn(Schema):
    attributes: List[int]
    product_id: int


class GameCarouselsMainSchema(Schema):
    items: List[ProductSchema]
    count: int
    next: bool
    previous: bool


class TabContentSchema(ModelSchema):
    class Meta:
        model = TabItem
        exclude = ["id", "title", "tab", "order"]
