# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "games"
implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import ModelSchema

from src.games.models import CatalogPage, Game
from src.products.models import Product


class CatalogPageSchema(ModelSchema):
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

    filters: List[CatalogPageSchema]

    class Meta:
        model = Game
        fields = "__all__"
        exclude = [
            "order",
        ]
