# -*- coding: utf-8 -*-
"""
    Module contains class for managing games and related
    to Games models.
"""
from typing import List

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase, api_controller

import src.products.schemas as product_schemas
from src.games.models import Game, CatalogTabs
from src.games.schemas import GamesSchema, SidebarSchema, CatalogPageSchema, WorthLookItemSchema, \
    CalendarBlockItemSchema, CalendarBlockSchema
from src.games.services.games_service import GameService


@api_controller("/games", tags=["Game"], permissions=[])
class GamesController(ControllerBase):
    """
    A controller class for managing games.
    This class provides endpoints for ordering, filtering,
    paginating and getting games and related entities of games.
    """

    def __init__(self, game_service: GameService):
        """
        Use this method to inject services to endpoints of GamesController
        :param game_service: variable for managing games and related entities
        """
        self.game_service = game_service

    @http_get("/product-carousels/", response=product_schemas.GameCarouselsMainSchema)
    def game_carousels(
            self,
            page: int,
            page_size: int,
            game_id: int,
            catalog_id: int = None,
    ) -> dict:
        """
        Endpoint gets all products for specific game, catalog_page
        if necessary and makes pagination of related queryset
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :param game_id: filter by game id
        :param catalog_id: filter(not required) additionally by catalog id
        :return:
        """
        result = self.game_service.get_games_carousel(
            game_id=game_id, catalog_id=catalog_id, page=page, page_size=page_size
        )
        return result

    @http_get("/{game_id}/catalog-pages/", response=List[SidebarSchema])
    def get_game_pages(self, game_id: int) -> QuerySet:
        """
        Endpoint gets all catalog's pages by game id.

        :return: dict
        """
        result = self.game_service.get_game_pages(game_id=game_id)
        return result

    @http_get("/", response=List[GamesSchema])
    def get_games(self) -> Game:
        """
        Endpoint gets all games and related
        to games root catalog pages
        :return:
        """
        result = self.game_service.get_games()
        return result


@api_controller("/catalog-page", tags=["Catalog"], permissions=[])
class CatalogController(ControllerBase):
    """
    A controller class for managing catalog.

    This class provides endpoints for ordering, filtering,
    paginating and getting games and related entities of catalog's pages.
    """

    def __init__(self, game_service: GameService):
        """
        Use this method to inject services to endpoints of CatalogController

        :param game_service: variable for managing games and related entities
        """
        self.game_service = game_service

    @http_get("/{page_id}/", response=CatalogPageSchema)
    def get_catalog_page(self, page_id: int) -> QuerySet:
        """
        Endpoint gets catalog's page content by page id.

        :return: dict
        """
        result = self.game_service.get_catalog_page(page_id=page_id)
        return result

    @http_get("/{page_id}/worth-look/", response=List[WorthLookItemSchema])
    def get_worth_look(self, page_id: int) -> QuerySet:
        """
        Endpoint gets catalog's page content by page id.

        :return: dict
        """
        result = self.game_service.get_worth_look(page_id=page_id)
        return result

    @http_get("/{page_id}/calendar/",
              response=List[CalendarBlockSchema])
    def get_calendar(self, page_id: int) -> QuerySet:
        """
        Endpoint gets catalog's calendar by page id.

        :return: dict
        """
        result = self.game_service.get_calendar(page_id=page_id)
        return result

    @http_get("/{block_id}/calendar-items/",
              response=List[CalendarBlockItemSchema])
    def get_calendar_items(self, block_id: int) -> QuerySet:
        """
        Endpoint gets calendar's content by block id.

        :return: dict
        """
        result = self.game_service.get_calendar_items(block_id=block_id)
        return result

    @http_get("/tab-content/{tab_id}/", response=product_schemas.TabContentSchema)
    def get_tab_content(self, request: HttpRequest, tab_id: int) \
            -> CatalogTabs:
        """
        Endpoint returns specific CatalogTabs model instance.

        :param request:
        :rtype: CatalogTabs()
        :param tab_id: id of CatalogTabs model's instance we want to get
        :return: return CatalogTabs() model instance
        """
        result = self.game_service.get_tab_content(tab_id=tab_id)
        return result
