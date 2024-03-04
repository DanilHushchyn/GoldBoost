from typing import List, Any

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ninja.pagination import paginate, PageNumberPagination, PaginationBase
from ninja_extra import Router, http_get, http_post, route

from ninja_extra.controllers.base import ControllerBase, api_controller
from ninja_jwt.authentication import JWTAuth

from src.games.services.games_service import GameService
import src.main.schemas as main_schemas
from src.main.models import Review

from src.main.services.main_service import MainService

from src.products.services.product_service import ProductService


@api_controller('/main', tags=['Main'], permissions=[])
class MainController(ControllerBase):
    def __init__(self, main_service: MainService):
        self.main_service = main_service

    # @http_get('/page/', response=main_schemas.MainPageSchema)
    # def get_main_page(self, ):
    #     result = self.main_service.get_main()
    #     result['games'] = self.game_service.get_games_for_main()
    #     result['hot_offers'] = self.product_service.hot_products_main()
    #     result['game_logos'] = self.game_service.get_games()
    #     return result

    @http_get('/reviews/', response=main_schemas.ReviewsSectionSchema)
    def get_reviews(self, page: int, page_size: int):
        result = self.main_service.get_reviews(page, page_size)
        return result

    @http_get('/why-choose-us/', response=List[main_schemas.WhyChooseUsSchema])
    def get_why_choose_us(self):
        result = self.main_service.get_why_choose_us()
        return result

    @http_get('/instagram/', response=List[main_schemas.InstaSchema])
    def get_instagram(self):
        result = self.main_service.get_instagram()
        return result

    @http_get('/news/', response=main_schemas.NewsSectionSchema)
    def get_news(self, page: int, page_size: int):
        result = self.main_service.get_news(page, page_size)
        return result

    @http_get('/settings/', response=main_schemas.SettingsOutSchema, auth=JWTAuth())
    def get_settings(self):
        result = self.main_service.get_settings()
        return result
