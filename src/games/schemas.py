# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "games"
implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import ModelSchema

from config.settings import ABSOLUTE_URL
from src.games.models import CatalogPage, Game, WorthLookItem, CalendarBlockItem, CalendarBlock, CatalogTabs
from src.products.models import Product


class FilterSchema(ModelSchema):
    """
    Pydantic schema for model CatalogPage.
    Purpose of this schema to return filters
    for game carousels on main page in the site
    """

    class Meta:
        model = CatalogPage
        fields = ["id", "title"]


class GameLogosProductSchema(ModelSchema):
    """
    Pydantic schema for model CatalogPage.
    Purpose of this schema to return filters
    for game carousels on main page in the site
    """

    @staticmethod
    def resolve_logo_product(obj):
        return ABSOLUTE_URL + obj.logo_product.url

    class Meta:
        model = Game
        fields = ["name", "logo_product"]


class GamesSchema(ModelSchema):
    """
    Pydantic schema for model Game.
    Purpose of this schema to return
    all games in the site and related to
    game CatalogPages queryset
    """

    filters: List[FilterSchema]

    @staticmethod
    def resolve_logo_filter(obj):
        return ABSOLUTE_URL + obj.logo_filter.url

    @staticmethod
    def resolve_logo_product(obj):
        return ABSOLUTE_URL + obj.logo_product.url

    class Meta:
        model = Game
        fields = "__all__"
        exclude = [
            "order",
        ]


class CatalogTabSchema(ModelSchema):
    """
    Pydantic schema for CatalogTabs.

    Purpose of this schema to return
    Filter model instance and related CatalogTabs
    queryset
    """

    class Meta:
        model = CatalogTabs
        fields = "__all__"
        exclude = ['content', 'catalog', 'order']


class CatalogPageSchema(ModelSchema):
    """
    Pydantic schema for model CatalogPage.

    Purpose of this schema to return
    info for catalog's page in the site
    """
    game_logo: str
    tabs: List[CatalogTabSchema]

    @staticmethod
    def resolve_game_logo(obj):
        return ABSOLUTE_URL + obj.game.logo_product.url

    class Meta:
        model = CatalogPage
        fields = ["title", "description"]


class SidebarSchema(ModelSchema):
    """
    Pydantic schema for model CatalogPage.

    Purpose of this schema to return links
    for sidebar
    """
    items: List["SidebarSchema"] | None

    class Meta:
        model = CatalogPage
        fields = ["id", "title"]


class CalendarBlockSchema(ModelSchema):
    """
    Pydantic schema for model CalendarBlock.

    Purpose of this schema to return
    calendar structure
    """

    class Meta:
        model = CalendarBlock
        exclude = ["calendar", ]


class CalendarBlockItemSchema(ModelSchema):
    """
    Pydantic schema for model CalendarBlockItem.

    Purpose of this schema to return
    calendar content
    """

    @staticmethod
    def resolve_team1_img(obj):
        return ABSOLUTE_URL + obj.team1_img.url

    @staticmethod
    def resolve_team2_img(obj):
        return ABSOLUTE_URL + obj.team2_img.url

    class Meta:
        model = CalendarBlockItem
        exclude = ["id", "block"]


class WorthLookItemSchema(ModelSchema):
    """
    Pydantic schema for model WorthLookItem.

    Purpose of this schema to return filters
    for game carousels on main page in the site
    """
    title: str
    offers: int

    @staticmethod
    def resolve_title(obj):
        return obj.catalog_page.title

    @staticmethod
    def resolve_image(obj):
        return ABSOLUTE_URL + obj.image.url

    @staticmethod
    def resolve_offers(obj):
        count = (Product.objects
                 .filter(catalog_page=obj.catalog_page)
                 .count())
        return count

    class Meta:
        model = WorthLookItem
        fields = ["catalog_page", "image", "image_alt"]
