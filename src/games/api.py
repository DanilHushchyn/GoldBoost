# -*- coding: utf-8 -*-
"""
    Module contains class for managing games and related.

    to Games models.
"""
from typing import List

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase, api_controller

import src.products.schemas as product_schemas
from src.games.models import CatalogTabs, Game
from src.games.schemas import (
    CalendarBlockItemSchema,
    CalendarBlockSchema,
    CatalogPageSchema,
    GamesSchema,
    SidebarSchema,
    WorthLookItemSchema,
)
from src.games.services.games_service import GameService
from src.main.utils import LangEnum
from ninja import Header


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
        :param game_service: variable for managing games
        and related entities
        """
        self.game_service = game_service

    @http_get(
        "/product-carousels/",
        response=product_schemas.GameCarouselsMainSchema,
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def game_carousels(
            self,
            request: HttpRequest,
            page: int,
            page_size: int,
            game_id: int,
            catalog_id: int = None,
            accept_lang:
            LangEnum = Header(alias='Accept-Language'),
    ) -> dict:
        """
        Get all products for specific game and catalog's page.

        Makes pagination

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page
         - **game_id** id of game, for filtering
         - **catalog_id** id of catalog's page, for filtering (it's optional)

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.game_service.get_games_carousel(
            game_id=game_id, catalog_id=catalog_id, page=page, page_size=page_size
        )
        return result

    @http_get(
        "/{game_id}/catalog-pages/",
        response=List[SidebarSchema],
        openapi_extra={
            404: {
                "description": "Error: Not Found",
                "content": {
                    "application/json": {
                        "schema": {
                            "properties": {
                                "detail": {
                                    "type": "string",
                                }
                            },
                            "example": {"detail": "Not Found: " "No Game matches " "the given query."},
                        }
                    }
                },
            },
            422: {
                "description": "Error: Unprocessable Entity",
                "content": {
                    "application/json": {
                        "schema": {
                            "properties": {
                                "detail": {
                                    "type": "string",
                                }
                            },
                        }
                    }
                },
            },
            "responses": {
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_game_pages(self, request: HttpRequest, game_id: int,
                       accept_lang:
                       LangEnum = Header(alias='Accept-Language'),
                       ) -> QuerySet:
        """
        Gets all catalog's pages by game id.


        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.game_service.get_game_pages(game_id=game_id)
        return result

    @http_get(
        "/",
        response=List[GamesSchema],
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Not Found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Not Found: " "No CatalogPage matches " "the given query."},
                            }
                        }
                    },
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_games(self, request: HttpRequest,
                  accept_lang:
                  LangEnum = Header(alias='Accept-Language'),
                  ) -> Game:
        """
        Get all games and related to specific game root catalog's pages.


        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

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

    @http_get(
        "/{page_id}/",
        response=CatalogPageSchema,
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Not Found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Not Found: " "No CatalogPage matches " "the given query."},
                            }
                        }
                    },
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_catalog_page(self, request: HttpRequest, page_id: int,
                         accept_lang:
                         LangEnum = Header(alias='Accept-Language'),
                         ) -> QuerySet:
        """
        Get catalog's page content by page id.

        Please provide:
         - **page_id**  id of page we want to get

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.game_service.get_catalog_page(page_id=page_id)
        return result

    @http_get(
        "/{page_id}/worth-look/",
        response=List[WorthLookItemSchema],
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Not Found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Not Found: " "No CatalogPage matches " "the given query."},
                            }
                        }
                    },
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_worth_look(self, request: HttpRequest, page_id: int,
                       accept_lang:
                       LangEnum = Header(alias='Accept-Language'),
                       ) -> QuerySet:
        """
        Get catalog's page content by page id.
        Please provide:
         - **page_id**  id of page we want to get

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.game_service.get_worth_look(page_id=page_id)
        return result

    @http_get(
        "/{page_id}/calendar/",
        response=List[CalendarBlockSchema],
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_calendar(self, request: HttpRequest, page_id: int,
                     accept_lang:
                     LangEnum = Header(alias='Accept-Language'),
                     ) -> QuerySet:
        """
        Gets catalog's calendar blocks by page id.
        Please provide:
         - **page_id**  id of page we want to get

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.game_service.get_calendar(page_id=page_id)
        return result

    @http_get(
        "/{block_id}/calendar-items/",
        response=List[CalendarBlockItemSchema],
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_calendar_items(self, request: HttpRequest, block_id: int,
                           accept_lang:
                           LangEnum = Header(alias='Accept-Language'),
                           ) -> QuerySet:
        """
        Get calendar's content by calendar block id.

        Please provide:
         - **block_id**  id of page we want to get

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.game_service.get_calendar_items(block_id=block_id)
        return result

    @http_get(
        "/tab-content/{tab_id}/",
        response=product_schemas.TabContentSchema,
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Not Found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                                "example": {"detail": "Not Found: " "No CatalogTabs matches " "the given query."},
                            }
                        }
                    },
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "detail": {
                                        "type": "string",
                                    }
                                },
                            }
                        }
                    },
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_tab_content(self, request: HttpRequest, tab_id: int,
                        accept_lang:
                        LangEnum = Header(alias='Accept-Language'),
                        ) -> CatalogTabs:
        """
        Get tab's content for catalog's page by tab id .

        Please provide:
         - **tab_id**  id of tab we want to get

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found.
          - **422**: Error: Not Found.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.game_service.get_tab_content(tab_id=tab_id)
        return result
