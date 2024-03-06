# -*- coding: utf-8 -*-
"""
    Module contains class for managing games
    and related entities in the site
"""
from django.db.models import Prefetch

from src.games.models import CatalogPage, Game
from src.products.models import Product
from src.products.utils import paginate


class GameService:
    """
    A service class for managing games and related entities in the site.
    This class provides methods for ordering, filtering,
    paginating and getting games and related entities.
    """

    @staticmethod
    def get_games_carousel(
        game_id: int,
        page: int,
        page_size: int,
        catalog_id: int = None,
    ) -> dict:
        """
        Gets all products for game carousel
        and make pagination of result queryset

        :param game_id: filter by game id
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :param catalog_id: filter by related to game catalog_page
        :return: dict for pagination
        """
        items = Product.objects.filter(catalog_page__game=game_id)
        if catalog_id:
            items = items.filter(catalog_page=catalog_id)
        for item in items:
            items.game_logo = item.catalog_page.game.logo_product.url

        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def get_games() -> Game:
        """
        Gets all games(instances of model Game) queryset in the site
        and for each element of queryset
        also related queryset of filters(root catalog_pages)
        :return: Game queryset
        """
        pr2 = Prefetch("catalog_pages", queryset=CatalogPage.objects.filter(parent=None), to_attr="filters")
        objects = Game.objects.prefetch_related(pr2).all()
        return objects
