from django.db.models import Prefetch

from src.games.models import Game, CatalogPage
from src.products.models import Product
from src.products.utils import paginate


class GameService:
    @staticmethod
    def get_games_carousel(game_id: int, page: int, page_size: int, catalog_id: int = None, ):
        items = Product.objects.filter(catalog_page__game=game_id)
        if catalog_id:
            items = items.filter(catalog_page=catalog_id)
        for item in items:
            items.game_logo = item.catalog_page.game.logo_product.url

        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def get_games():
        pr2 = Prefetch('catalog_pages',
                       queryset=CatalogPage.objects.filter(parent=None),
                       to_attr='filters')
        objects = Game.objects.prefetch_related(pr2).all()
        return objects
