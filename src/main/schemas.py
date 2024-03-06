# -*- coding: utf-8 -*-
from typing import List

from ninja import ModelSchema, Schema

import src.games.schemas as game_schemas
from src.main.models import Insta, News, Review, Setting, WhyChooseUs


class WhyChooseUsSchema(ModelSchema):
    class Meta:
        model = WhyChooseUs
        fields = "__all__"
        exclude = ("id",)


class ReviewsSchema(ModelSchema):
    class Meta:
        model = Review
        fields = "__all__"


class NewsSchema(ModelSchema):
    game: game_schemas.GameLogosProductSchema

    class Meta:
        model = News
        fields = "__all__"


class InstaSchema(ModelSchema):
    class Meta:
        model = Insta
        fields = [
            "img",
        ]


class SettingsOutSchema(ModelSchema):
    class Meta:
        model = Setting
        fields = "__all__"
        exclude = ["subscribe_sale", "id"]


# class HotOfferSectionSchema(Schema):
#     items: List[CarouselProductsSchema]
#     count: int


class ReviewsSectionSchema(Schema):
    items: List[ReviewsSchema]
    count: int
    next: bool
    previous: bool


class NewsSectionSchema(Schema):
    items: List[NewsSchema]
    count: int
    next: bool
    previous: bool


# class MainPageSchema(Schema):
#     game_logos: List[game_schemas.GameLogosFilterSchema]
#     games: List[game_schemas.GameSchema]
#     why_choose_us: List[WhyChooseUsSchema]
#     hot_offers: HotOfferSectionSchema
#     reviews: ReviewsSectionSchema
#     news: NewsSectionSchema
#     instagram: List
