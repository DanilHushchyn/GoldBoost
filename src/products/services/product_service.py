from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum, Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from src.games.models import TabItem
from src.products.models import Product, SubFilter, Filter
from src.products.schemas import ProductCountPriceIn
from src.products.utils import paginate


class ProductService:
    """
    A service class for managing products.
    This class provides methods for ordering, filtering,
    paginating and getting related entities of products.
    """
    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        """
        This function for getting info product's card page.
        :param product_id: id of Product model's instance
        :return: Product model's instance with related filters
        """
        pr_filters = Prefetch('filters', queryset=Filter.objects.all(), )
        product = Product.objects.prefetch_related(pr_filters).get(id=product_id)
        return product

    @staticmethod
    def get_hot_products(page: int, page_size: int, game_id: int = None) -> dict:
        """
        Gets all products with Tag(related models) value hot
        and make pagination of related queryset
        :rtype: dict
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :param game_id: filter(not required) additionally hot products by game id
        :return: dict which contains all parameters for pagination
        """
        items = Product.objects.hot_all(game_id)
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def best_sellers(page: int, page_size: int) -> dict:
        """
        Gets all products ordered by bought_count field in
        model Product (return frequently bought products on site)
        :rtype: object
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains all parameters for pagination
        """
        items = Product.objects.bestsellers()
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def get_tab_content(tab_id: int) -> TabItem:
        """
        Returns specific TabItem model instance
        :rtype: TabItem()
        :param tab_id: id of TabItem model's instance we want to get
        :return: return TabItem() model instance
        """
        tab = get_object_or_404(TabItem, id=tab_id)
        return tab

    @staticmethod
    def get_tabs(product_id: int) -> QuerySet:
        """
        Returns TabItem's queryset filtered
        by id of related Product model's instance
        :rtype: QuerySet
        :param product_id: id of Product model instance
        :return: TabItem's queryset
        """
        tabs = TabItem.objects.filter(tab__product=product_id)
        return tabs
