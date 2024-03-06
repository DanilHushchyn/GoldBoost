# -*- coding: utf-8 -*-
from typing import List

from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase, api_controller

import src.products.schemas as product_schemas
from src.games.schemas import GamesSchema
from src.games.services.games_service import GameService


@api_controller("/games", tags=["Game"], permissions=[])
class GamesController(ControllerBase):
    def __init__(self, game_service: GameService):
        self.game_service = game_service

    @http_get("/product-carousels/", response=product_schemas.GameCarouselsMainSchema)
    def game_carousels(
        self,
        page: int,
        page_size: int,
        game_id: int,
        catalog_id=None,
    ):
        result = self.game_service.get_games_carousel(
            game_id=game_id, catalog_id=catalog_id, page=page, page_size=page_size
        )
        return result

    @http_get("/", response=List[GamesSchema])
    def get_games(self):
        result = self.game_service.get_games()
        return result
