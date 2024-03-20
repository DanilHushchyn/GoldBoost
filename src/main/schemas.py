# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "main".

Implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import ModelSchema, Schema

import src.games.schemas as game_schemas
from config.settings import ABSOLUTE_URL
from src.main.models import Insta, News, PromoCode, Review, Setting, WhyChooseUs


class WhyChooseUsSchema(ModelSchema):
    """
    Pydantic schema for model WhyChooseUs.

    Purpose of this schema to return WhyChooseUs
    queryset to client side
    """

    @staticmethod
    def resolve_icon(obj):
        return ABSOLUTE_URL + obj.icon.url

    class Meta:
        model = WhyChooseUs
        fields = "__all__"
        exclude = ("id",)


class ReviewsSchema(ModelSchema):
    """
    Pydantic schema for model Reviews.

    Purpose of this schema to return Reviews
    queryset to client side
    """

    class Meta:
        model = Review
        fields = "__all__"
        exclude = ("id",)


class NewsSchema(ModelSchema):
    """
    Pydantic schema for model News.

    Purpose of this schema to return News
    queryset to client side
    """

    game: game_schemas.GameLogosProductSchema

    @staticmethod
    def resolve_image(obj):
        return ABSOLUTE_URL + obj.image.url

    class Meta:
        model = News
        fields = "__all__"
        exclude = ("id",)


class InstaSchema(ModelSchema):
    """
    Pydantic schema for model Insta.

    Purpose of this schema to return Insta
    queryset to client side
    """

    @staticmethod
    def resolve_img(obj):
        return ABSOLUTE_URL + obj.img.url

    class Meta:
        model = Insta
        fields = ["img", "img_alt"]


class SettingsOutSchema(ModelSchema):
    """
    Pydantic schema for model Setting.

    Purpose of this schema to return Setting
    model instance data to client side
    """

    class Meta:
        model = Setting
        fields = "__all__"
        exclude = ["subscribe_sale", "id"]


class ReviewsSectionSchema(Schema):
    """
    Pydantic schema for section Reviews.

    Purpose of this schema to return
    paginated queryset of Review
    """

    items: List[ReviewsSchema]
    count: int
    next: bool
    previous: bool


class NewsSectionSchema(Schema):
    """
    Pydantic schema for section News.

    Purpose of this schema to return
    paginated queryset of News
    """

    items: List[NewsSchema]
    count: int
    next: bool
    previous: bool


class PromoCodeSchema(ModelSchema):
    class Meta:
        model = PromoCode
        fields = ["discount"]


class OrderOutSchema(Schema):
    """
    Pydantic schema for return message to client side.

    Purpose of this schema just say that operation
    has been successful
    """

    message: str | None
    auth_user: bool
