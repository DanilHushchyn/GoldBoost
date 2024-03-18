# -*- coding: utf-8 -*-
"""
    Module contains class for managing products on site
"""
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from src.orders.models import Cart, CartItem, Attribute
from src.products.models import Filter, Product, SubFilter, ProductTabs
from src.products.schemas import AddToCartSchema
from src.products.utils import paginate
from src.users.schemas import MessageOutSchema

User = get_user_model()


class ProductService:
    """
    A service class for managing products.

    This class provides methods for ordering, filtering,
    paginating and getting related entities of products.
    """

    @staticmethod
    def add_product_to_cart(product_id: int, user: User | str,
                            body: AddToCartSchema) \
            -> MessageOutSchema:
        """
        Gets info for product's card page.

        :param body: list of attributes
        :param user: user object or sessionKey
        for product with range price
        :param product_id: id of Product model's instance
        :return: Product model's instance with related filters
        """
        try:
            product = (Product.objects
                       .prefetch_related('filters__subfilters')
                       .get(id=product_id))
        except Product.DoesNotExist:
            raise HttpError(404, 'Product not found ☹')

        if isinstance(user, User):
            cart, status = Cart.objects.get_or_create(user=user)
        else:
            cart, status = (Cart.objects.
                            get_or_create(session_key=user))

        if product.price_type == 'range':
            attributes = set(body.attributes)
            for subfilter_id in attributes:
                get_object_or_404(SubFilter,
                                  id=subfilter_id,
                                  filter__product=product_id)
            filters = product.filters.exclude(type__in=['CheckBox'])
            for flt in filters:
                count = flt.subfilters.filter(id__in=attributes).count()
                if count != 1:
                    raise HttpError(403,
                                    'Sub filters has '
                                    'been chosen incorrectly ☹ '
                                    f'(Error: {flt.type} has {count}'
                                    f' chosen elements '
                                    f'but 1 have to be choosing)')
            cart_item = (CartItem.objects.
                         create(product=product,
                                quantity=body.quantity,
                                cart=cart))
            for subfilter_id in attributes:
                Attribute.objects.create(sub_filter_id=subfilter_id,
                                         cart_item=cart_item)

        if product.price_type == 'fixed':
            (CartItem.objects.
             create(product=product,
                    quantity=body.quantity,
                    cart=cart))

        return MessageOutSchema(
            message='Product added to cart successfully')

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        """
        Gets info for product's card page.

        :param product_id: id of Product model's instance
        :return: Product model's instance with related filters
        """
        pr_filters = Prefetch(
            "filters",
            queryset=Filter.objects.all(),
        )
        try:
            product = (Product.objects.
                       prefetch_related(pr_filters).
                       get(id=product_id))
        except Product.DoesNotExist:
            raise HttpError(404, "Product not found ☹")
        return product

    @staticmethod
    def get_hot_products(page: int,
                         page_size: int,
                         game_id: int = None) -> dict:
        """
        Gets all products with Tag(related models) value hot.

        Also makes pagination of related queryset
        :rtype: dict
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :param game_id: filter(not required) additionally by game id
        :return: dict which contains all parameters for pagination
        """
        items = Product.objects.hot_all(game_id)
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def best_sellers(page: int, page_size: int) -> dict:
        """
        Gets all products ordered by bought_count field.

        (return frequently bought products on site)
        :rtype: object
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains all parameters for pagination
        """
        items = Product.objects.bestsellers()
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def get_tab_content(tab_id: int) -> ProductTabs:
        """
        Returns specific ProductTabs model instance.

        :rtype: ProductTabs()
        :param tab_id: id of TabItem model's instance we want to get
        :return: return ProductTabs() model instance
        """
        tab = get_object_or_404(ProductTabs, id=tab_id)
        return tab

    @staticmethod
    def search_products(search_line: str, game_id: int = None) \
            -> QuerySet:
        """
        Gets all products with Tag(related models) value hot.

        Also makes pagination of related queryset
        :param search_line: parameter for searching
        :rtype: dict
        :param game_id: filter(not required) additionally by game id
        :return: dict which contains all parameters for pagination
        """
        if game_id:
            items = Product.objects.filter(catalog_page__game_id=game_id,
                                           title__icontains=search_line)
        else:
            items = Product.objects.filter(title__icontains=search_line)
        return items[:10]
