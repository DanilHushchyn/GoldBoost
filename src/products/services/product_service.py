# -*- coding: utf-8 -*-
"""
    Module contains class for managing products on site.

"""
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from ninja.errors import HttpError

from src.orders.models import Attribute, Cart, CartItem
from src.orders.services.order_service import OrderService
from src.products.models import Filter, FreqBought, Product, ProductTabs, SubFilter
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
    def add_product_to_cart(product_id: int, request: HttpRequest, body: AddToCartSchema) -> MessageOutSchema:
        """
        Gets info for product's card page.

        :param request: HttpRequest
        :param body: list of attributes
        for product with range price
        :param product_id: id of Product model's instance
        :return: Product model's instance with related filters
        """
        try:
            product = Product.objects.prefetch_related("filters__subfilters").get(id=product_id)
        except Product.DoesNotExist:
            raise HttpError(404, _("Not Found: No Product" " matches the given query."))
        cart = OrderService().get_my_cart(request=request)
        if product.price_type == "range":
            attributes = set(body.attributes)
            for subfilter_id in attributes:
                get_object_or_404(SubFilter, id=subfilter_id, filter__product=product_id)
            filters = product.filters.exclude(type__in=["CheckBox"])
            for flt in filters:
                count = flt.subfilters.filter(id__in=attributes).count()
                if count != 1:
                    raise HttpError(
                        403,
                        _(
                            "Sub filters has "
                            "been chosen incorrectly "
                            f"(Error: {flt.type} has {count}"
                            f" chosen elements "
                            f"but 1 have to be choosing)"
                        ),
                    )

            create_item = True
            cart_items = cart.items.filter(product=product)
            for cart_item in cart_items:
                attrs = cart_item.attributes.values_list("sub_filter_id", flat=True)
                attrs1 = set(attrs)
                attrs2 = set(body.attributes)
                if attrs1 == attrs2:
                    total_q = cart_item.quantity + body.quantity
                    cart_item.quantity = total_q
                    cart_item.save()
                    create_item = False
                    break
            if create_item:
                cart_item = CartItem.objects.create(product=product, quantity=body.quantity, cart=cart)
                for subfilter_id in attributes:
                    Attribute.objects.create(sub_filter_id=subfilter_id, cart_item=cart_item)
        if product.price_type == "fixed":
            try:
                cart_item = cart.items.get(product=product)
                cart_item.quantity = cart_item.quantity + body.quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                (CartItem.objects.create(product=product, quantity=body.quantity, cart=cart))
        return MessageOutSchema(message=_("Product added to cart " "successfully"))

    @staticmethod
    def get_product_by_id(request: HttpRequest, product_id: int) -> Product:
        """
        Gets info for product's card page.

        :param request:
        :param product_id: id of Product model's instance
        :return: Product model's instance with related filters
        """
        pr_filters = Prefetch(
            "filters",
            queryset=Filter.objects.all(),
        )
        try:
            product = Product.objects.prefetch_related(pr_filters).get(id=product_id)
        except Product.DoesNotExist:
            raise HttpError(404, _("Not Found: No Product matches" " the given query."))
        return product

    @staticmethod
    def get_hot_products(page: int, page_size: int, game_id: int = None) -> dict:
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
    def frequently_bought() -> QuerySet:
        """
        Gets products which frequently bought together.

        (return frequently bought products on site)
        :return: FreqBoughtSchema , all orders for
        bought product together
        """
        items = FreqBought.objects.prefetch_related("products").all()
        return items

    @staticmethod
    def get_tab_content(tab_id: int) -> ProductTabs:
        """
        Returns specific ProductTabs model instance.

        :rtype: ProductTabs()
        :param tab_id: id of TabItem model's instance we want to get
        :return: return ProductTabs() model instance
        """
        try:
            tab = ProductTabs.objects.get(id=tab_id)
        except ProductTabs.DoesNotExist:
            raise HttpError(404, _("Not Found: No ProductTabs matches" " the given query."))
        return tab

    @staticmethod
    def search_products(search_line: str, game_id: int = None) -> QuerySet:
        """
        Gets all products with Tag(related models) value hot.

        Also makes pagination of related queryset
        :param search_line: parameter for searching
        :rtype: dict
        :param game_id: filter(not required) additionally by game id
        :return: dict which contains all parameters for pagination
        """
        items = Product.objects.filter(Q(title_en__icontains=search_line) | Q(title_uk__icontains=search_line))

        if game_id:
            items = items.filter(catalog_page__game_id=game_id)
        return items[:10]

    @staticmethod
    def freqbot_to_cart(freqbot_id: int, request: HttpRequest) -> MessageOutSchema:
        cart = OrderService().get_my_cart(request=request)
        try:
            freqbot = FreqBought.objects.get(id=freqbot_id)
        except FreqBought.DoesNotExist:
            raise HttpError(404, _("Not Found: No FreqBought matches" " the given query."))

        try:
            cart_item = cart.items.get(freqbot=freqbot)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(freqbot_id=freqbot.id, quantity=1, cart_id=cart.id)
        return MessageOutSchema(message=_("Freqbot element added to cart " "successfully"))
