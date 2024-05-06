# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "games"
implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import ModelSchema, Field

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


class GameLogosFilterSchema(ModelSchema):
    """
    Pydantic schema for model Game.
    Purpose of this schema to return filter logo
    for news carousel on main page in the site
    """
    logo: str | None

    @staticmethod
    def resolve_logo(obj):
        return ABSOLUTE_URL + obj.logo_filter.url

    class Meta:
        model = Game
        fields = ["name"]


class GamesSchema(ModelSchema):
    """
    Pydantic schema for model Game.
    Purpose of this schema to return
    all games in the site and related to
    game CatalogPages queryset
    """

    items: List[FilterSchema]

    @staticmethod
    def resolve_logo_filter(obj):
        return ABSOLUTE_URL + obj.logo_filter.url

    @staticmethod
    def resolve_logo_product(obj):
        return ABSOLUTE_URL + obj.logo_product.url

    class Meta:
        model = Game
        fields = [
            'id',
            'name',
            'logo_filter',
            'logo_product',
            'logo_filter_alt',
            'logo_product_alt',
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
        fields = ['id', 'title', ]


class CatalogPageSchema(ModelSchema):
    """
    Pydantic schema for model CatalogPage.

    Purpose of this schema to return
    info for catalog's page in the site
    """
    game_logo: str
    game_logo_alt: str
    game_id: int
    tabs: List[CatalogTabSchema]

    @staticmethod
    def resolve_game_logo(obj):
        return ABSOLUTE_URL + obj.game.logo_product.url

    @staticmethod
    def resolve_game_id(obj):
        return obj.game.id

    @staticmethod
    def resolve_game_logo_alt(obj):
        return obj.game.logo_product_alt

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
        fields = ['id', "title", 'subtitle']


class CalendarBlockItemSchema(ModelSchema):
    """
    Pydantic schema for model CalendarBlockItem.

    Purpose of this schema to return
    calendar content
    """
    team1_img: str
    team1_img_alt: str = Field(None, alias="team1.team_img_alt")
    team2_img: str
    team2_img_alt: str = Field(None, alias="team2.team_img_alt")

    @staticmethod
    def resolve_team1_img(obj):
        return ABSOLUTE_URL + obj.team1.team_img.url

    @staticmethod
    def resolve_team2_img(obj):
        return ABSOLUTE_URL + obj.team2.team_img.url

    class Meta:
        model = CalendarBlockItem
        fields = [
            'date',
            'team1_from',
            'team1_until',
            'team2_from',
            'team2_until',
        ]


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
        # count = (Product.objects
        #          .filter(catalog_page=obj.catalog_page)
        #          .count())
        # print(obj.catalog_page.products.count())
        return obj.catalog_page.products.count()

    class Meta:
        model = WorthLookItem
        fields = ["catalog_page", "image", "image_alt"]
