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
        fields = ['icon', 'icon_alt', 'title', 'description']


class ReviewsSchema(ModelSchema):
    """
    Pydantic schema for model Reviews.

    Purpose of this schema to return Reviews
    queryset to client side
    """

    class Meta:
        model = Review
        fields = ['author',
                  'comment',
                  'stars_count',
                  'source_of_review_url',
                  'date_published',
                  'source_of_review']


class NewsSchema(ModelSchema):
    """
    Pydantic schema for model News.

    Purpose of this schema to return News
    queryset to client side
    """

    game: game_schemas.GameLogosFilterSchema

    @staticmethod
    def resolve_image(obj):
        return ABSOLUTE_URL + obj.image.url

    class Meta:
        model = News
        fields = [
            'title',
            'image',
            'image_alt',
            'description',
            'date_published',
        ]


class InstaSchema(ModelSchema):
    """
    Pydantic schema for model Insta.

    Purpose of this schema to return Insta
    queryset to client side
    """
    img_thumbnail: str | None = None

    @staticmethod
    def resolve_img(obj):
        return ABSOLUTE_URL + obj.img.url

    @staticmethod
    def resolve_img_thumbnail(obj):
        return ABSOLUTE_URL + obj.img_thumbnail.url

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
        fields = [
            'instagram_nickname',
            'instagram_link',
            'facebook_link',
            'reddit_link',
            'email',
            'discord_link',
            'whats_up_link',
            'header_top_text',
            'footer_bottom_text',
            'footer_description',
            'privacy_policy_link',
            'terms_of_use_link',
            'refund_policy_link',
            'address1',
            'address1_link',
            'address2',
            'address2_link',
            'subscribe_form_text',
            'subscribe_sale',
        ]


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
    discount: int

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
