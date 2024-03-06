# -*- coding: utf-8 -*-
"""
    Module contains class for managing games and related
    to Games models.
"""
from typing import List

from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase, api_controller

import src.products.schemas as product_schemas
from src.games.models import Game
from src.games.schemas import GamesSchema
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

    @http_get("/", response=List[GamesSchema])
    def get_games(self) -> Game:
        """
        Endpoint gets all games and related
        to games root catalog pages
        :return:
        """
        result = self.game_service.get_games()
        return result
