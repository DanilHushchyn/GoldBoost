from typing import List

from ninja import ModelSchema

from src.games.models import Game, CatalogPage
from src.products.models import Product


class CatalogPageSchema(ModelSchema):
    class Meta:
        model = CatalogPage
        fields = ['id', 'title']


class ProductPageSchema(ModelSchema):
    # tag: TagOutSchema = None
    price_from: int | None
    price_to: int | None
    sale_period: str | None
    sale_active: bool
    sale_price_from: float | None
    sale_price_to: float | None
    sale_price: float | None

    class Meta:
        model = Product
        fields = ['id', 'title', 'subtitle', 'card_img', 'price', 'price_type', 'sale_percent']


class GameSchema(ModelSchema):
    pages: List[CatalogPageSchema]
    items: List[ProductPageSchema]
    count: int | None

    class Meta:
        model = Game
        fields = '__all__'


class GameLogosFilterSchema(ModelSchema):
    class Meta:
        model = Game
        fields = ['id', 'logo_filter']


class GameLogosProductSchema(ModelSchema):
    class Meta:
        model = Game
        fields = ['name', 'logo_product']


class GamesSchema(ModelSchema):
    filters: List[CatalogPageSchema]

    class Meta:
        model = Game
        fields = '__all__'
        exclude = ['order',]