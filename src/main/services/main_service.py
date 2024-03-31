# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model


from src.main.models import Insta, News, PromoCode, Review, Setting, WhyChooseUs
from src.products.utils import paginate
from django.utils.translation import gettext as _

User = get_user_model()


class MainService:
    """
    A service class for managing common entities on the site.
    This class provides methods for ordering, filtering,
    paginating and common entities on the site.
    """

    @staticmethod
    def get_why_choose_us() -> WhyChooseUs:
        """
        Gets data for section WhyChooseUs
        on main page of the site
        :return: WhyChooseUs model queryset
        :rtype: WhyChooseUs
        """
        # activate('en')
        objects = WhyChooseUs.objects.all()
        return objects

    @staticmethod
    def get_instagram() -> Insta:
        """
        Gets data for section instagram
        on main page of the site
        :return: Insta model queryset
        :rtype: Insta
        """
        objects = Insta.objects.all()
        return objects

    @staticmethod
    def get_reviews(page: int, page_size: int) -> dict:
        """
        Gets data for section Reviews
        on main page of the site
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains parameters for pagination
        :rtype: dict
        """
        items = Review.objects.all()
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def get_settings() -> Setting:
        """
        Gets data for footer and header of the site
        :return: Setting model instance
        :rtype: Setting
        """
        return Setting.objects.first()

    @staticmethod
    def get_news(page: int, page_size: int) -> dict:
        """
        Gets data for section News
        on main page of the site
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains parameters for pagination
        :rtype: dict
        """
        items = News.objects.all()
        return paginate(items=items, page=page, page_size=page_size)
