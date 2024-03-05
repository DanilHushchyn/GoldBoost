from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404

from src.main.models import WhyChooseUs, Review, News, Insta, Setting
from src.products.models import Product
from src.products.utils import paginate


class MainService:
    """
    A service class for managing common entities on the site.
    This class provides methods for ordering, filtering,
    paginating and common entities on the site.
    """

    @staticmethod
    def get_why_choose_us() -> WhyChooseUs:
        """
        Getting data for section WhyChooseUs
        on main page of the site
        """
        objects = WhyChooseUs.objects.all()
        return objects

    @staticmethod
    def get_instagram() -> Insta:
        """
        Getting data for section instagram
        on main page of the site
        """
        objects = Insta.objects.all()
        return objects

    @staticmethod
    def get_reviews(page: int, page_size: int) -> dict:
        """
        Getting data for section Reviews
        on main page of the site
        """
        items = Review.objects.all()
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def get_settings() -> Setting:
        """
        Getting data for footer and header of the site
        """
        return Setting.objects.first()

    @staticmethod
    def get_news(page: int, page_size: int) -> dict:
        """
        Getting data for section News
        on main page of the site
        """
        items = News.objects.all()
        return paginate(items=items, page=page, page_size=page_size)
