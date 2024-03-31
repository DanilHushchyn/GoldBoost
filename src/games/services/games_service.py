# -*- coding: utf-8 -*-
"""
    Module contains class for managing games and related entities.

"""
from django.db.models import Prefetch, QuerySet
from ninja.errors import HttpError

from src.games.models import CalendarBlock, CalendarBlockItem, CatalogPage, CatalogTabs, Game
from src.products.models import Product
from src.products.utils import paginate
from django.utils.translation import gettext as _


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
        Gets all products for game carousel.

        Make pagination of result queryset

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
        Gets all games(instances of model Game) queryset in the site.

        and for each element of queryset
        also related queryset of filters(root catalog_pages)
        :return: Game queryset
        """
        pr2 = Prefetch("catalog_pages",
                       queryset=CatalogPage.objects.filter(parent=None),
                       to_attr="filters")
        objects = Game.objects.prefetch_related(pr2).all()
        return objects

    @staticmethod
    def get_game_pages(game_id: int) -> QuerySet:
        """
        Gets all catalog's pages for specific game by game id.

        :param game_id: id of game
        :return: QuerySet of root pages related to game
        """
        try:
            Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No Game matches"
                              " the given query."))
        pages = CatalogPage.objects.prefetch_related("items").filter(game_id=game_id, parent=None)
        return pages

    @staticmethod
    def get_catalog_page(page_id: int) -> CatalogPage:
        """
        Gets content for specific page by page id.

        :param page_id: id of page
        :return: CatalogPage model instance
        """
        try:
            page = CatalogPage.objects.get(id=page_id)
        except CatalogPage.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No CatalogPage matches"
                              " the given query."))
        return page

    @staticmethod
    def get_worth_look(page_id: int) -> QuerySet:
        """
        Gets content for specific page by page id.

        :param page_id: id of page
        :return: CatalogPage model instance
        """
        try:
            page = CatalogPage.objects.get(id=page_id)
        except CatalogPage.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No CatalogPage matches"
                              " the given query."))
        worth_look = page.worth_look
        if worth_look:
            return worth_look.items
        raise HttpError(404, _("Not found section WorthLook" " for this catalog's page"))

    @staticmethod
    def get_calendar(page_id: int) -> QuerySet:
        """
        Returns Calendar blocks.

        Filtered by id of related Product model's instance
        :param page_id: id of CatalogPage model instance
        :rtype: QuerySet
        :return: TabItem's queryset
        """
        items = CalendarBlock.objects.filter(calendar__catalogpage=page_id)
        return items

    @staticmethod
    def get_calendar_items(block_id: int) -> QuerySet:
        """
        Returns TabItem's queryset.

        Filtered by id of related Product model's instance
        :param block_id:
        :rtype: QuerySet
        :return: TabItem's queryset
        """
        items = CalendarBlockItem.objects.filter(block=block_id)
        return items

    @staticmethod
    def get_tab_content(tab_id: int) -> CatalogTabs:
        """
        Returns specific ProductTabs model instance.

        :rtype: CatalogTabs()
        :param tab_id: id of TabItem model's instance we want to get
        :return: return CatalogTabs() model instance
        """
        try:
            tab = CatalogTabs.objects.get(id=tab_id)
        except CatalogTabs.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No CatalogTab matches"
                              " the given query."))
        return tab
