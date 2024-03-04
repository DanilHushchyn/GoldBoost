from datetime import timedelta

from src.games.models import TabItem, Game, Tab
from src.products.models import Product, SubFilter, Filter, Tag
from ninja import Schema, Form
from ninja import ModelSchema
from typing import List


class TagOutSchema(ModelSchema):
    class Meta:
        model = Tag
        fields = '__all__'
        exclude = ('id',)


class ProductSchema(ModelSchema):
    tag: TagOutSchema | None
    price_from: float | None
    price_to: float | None
    sale_price_from: float | None
    sale_price_to: float | None
    sale_price: float | None
    sale_period: str | None
    sale_active: bool

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('bought_count', 'tab')


# class CarouselProductsSchema(ModelSchema):
#     tag: TagOutSchema | None
#     game_logo: str
#     price_from: float | None
#     price_to: float | None
#     sale_price_from: float | None
#     sale_price_to: float | None
#     sale_price: float | None
#     sale_period: str | None
#     sale_active: bool
#
#     class Meta:
#         model = Product
#         fields = ['title', 'subtitle', 'card_img', 'price', 'price_type', 'sale_percent']
#

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
        fields = '__all__'
        exclude = ('tab', 'content', 'order')


class TabSchema(ModelSchema):
    tab_items: List[TabItemSchema] | None

    class Meta:
        model = Tab
        fields = '__all__'
        exclude = ('id',)


class SubFilterItemSchema(ModelSchema):
    class Meta:
        model = SubFilter
        fields = '__all__'
        exclude = ('filter',)


class FilterItemSchema(ModelSchema):
    subfilters: List[SubFilterItemSchema]

    class Meta:
        model = Filter
        fields = '__all__'
        exclude = ('id', 'product')

class ProductCardSchema(ModelSchema):
    filters: List[FilterItemSchema] | None
    # tab: TabSchema | None
    price_from: float | None
    price_to: float | None
    sale_price_from: float | None
    sale_price_to: float | None
    sale_price: float | None
    sale_period: str | None
    sale_active: bool

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('bought_count', 'tag')


# class ProductCardOutSchema(Schema):
#     product: ProductCardSchema
# tabs: List[TabItemSchema] | None
# filters: List[FilterItemSchema] | None


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
        exclude = ['id', 'title', 'tab','order']
