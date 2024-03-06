# -*- coding: utf-8 -*-
"""
    Module contains class for managing managing common entities on site
"""
# -*- coding: utf-8 -*-
from typing import List

from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase, api_controller

import src.main.schemas as main_schemas
from src.main.models import Insta, Setting, WhyChooseUs
from src.main.services.main_service import MainService


@api_controller("/main", tags=["Main"], permissions=[])
class MainController(ControllerBase):
    """
    A controller class for managing common entities on site.
    This class provides endpoints for ordering, filtering
    and paginating common entities on site.
    """

    def __init__(self, main_service: MainService):
        """
        Use this method to inject services to endpoints of MainController
        :param main_service: variable for managing common entities
        """
        self.main_service = main_service

    @http_get("/reviews/", response=main_schemas.ReviewsSectionSchema)
    def get_reviews(self, page: int, page_size: int) -> dict:
        """
        Endpoint to get data for section Reviews
        on main page of the site
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains parameters for pagination
        :rtype: dict
        """
        result = self.main_service.get_reviews(page, page_size)
        return result

    @http_get("/why-choose-us/", response=List[main_schemas.WhyChooseUsSchema])
    def get_why_choose_us(self) -> WhyChooseUs:
        """
        Endpoint to gets data for section WhyChooseUs
        on main page of the site
        :return: WhyChooseUs model queryset
        :rtype: WhyChooseUs
        """
        result = self.main_service.get_why_choose_us()
        return result

    @http_get("/instagram/", response=List[main_schemas.InstaSchema])
    def get_instagram(self) -> Insta:
        """
        Endpoint to gets data for section Instagram
        on main page of the site
        :return: Insta model queryset
        :rtype: Insta
        """
        result = self.main_service.get_instagram()
        return result

    @http_get("/news/", response=main_schemas.NewsSectionSchema)
    def get_news(self, page: int, page_size: int) -> dict:
        """
        Endpoint to gets data for section News
        on main page of the site
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains parameters for pagination
        :rtype: dict
        """
        result = self.main_service.get_news(page, page_size)
        return result

    @http_get("/settings/", response=main_schemas.SettingsOutSchema)
    def get_settings(self) -> Setting:
        """
        Endpoint to get data for footer and header of the site
        :return: Setting model instance
        :rtype: Setting
        """
        result = self.main_service.get_settings()
        return result
