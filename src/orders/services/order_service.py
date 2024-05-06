# -*- coding: utf-8 -*-
"""
    Module contains class for managing orders on site
"""
import random
from typing import Tuple, Any

from django.contrib.auth import get_user_model

# -*- coding: utf-8 -*-
from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from ninja.errors import HttpError

from src.main.models import OrderItem, OrderItemAttribute, PromoCode, Setting
from src.main.schemas import OrderOutSchema
from src.main.services.main_service import MainService
from src.orders.models import Cart, CartItem, Order
from src.orders.tasks import change_order_status
from src.products.utils import make_sale, paginate
from src.users.schemas import MessageOutSchema
from loguru import logger
from django.core.cache import cache

User = get_user_model()


class OrderService:
    """
    A service class for managing orders.

    This class provides methods for ordering, filtering,
    paginating and getting related entities of orders.
    """

    @staticmethod
    def get_my_cart(request: HttpRequest) -> Cart:
        """
        Gets info for user's cart.

        :param request: HttpRequest
        :return: Cart model instance
        """
        if not request.auth.is_anonymous:
            user = request.auth
            cart, status = (Cart.objects
                            .prefetch_related(
                                "items__product__catalog_page__game",
                                "items__attributes__sub_filter__filter",
                                "items__freqbot__products__catalog_page__game",
                            )
                            .get_or_create(user=user))
        else:
            session_id = request.session.session_key
            if session_id is None:
                request.session.create()
                request.session.save()
                session_id = request.session.session_key
            cart, status = (Cart.objects
                            .prefetch_related(
                                "items__product__catalog_page__game",
                                "items__attributes__sub_filter__filter",
                                "items__freqbot__products__catalog_page__game",
                            )
                            .get_or_create(
                                session_key=session_id
                            ))
        return cart

    def delete_cart_item(self, request: HttpRequest, item_id: int) -> MessageOutSchema:
        """
        Delete cart's item it's by id.

        :param request: HttpRequest
        :param item_id: cart's item id
        :return: Cart model instance
        """
        cart = self.get_my_cart(request=request)
        try:
            item = CartItem.objects.get(cart_id=cart.id, id=item_id)
        except CartItem.DoesNotExist:
            raise HttpError(404, _("Not Found: No CartItem matches" " the given query."))
        item.delete()
        return MessageOutSchema(message=_("Cart items has been deleted successfully"))

    @staticmethod
    def create_number():
        while True:
            num = random.randint(100_000_000, 999_999_999)
            if not Order.objects.filter(number=num).exists():
                break
        return num

    @staticmethod
    def calc_total(cart: Cart) -> [float, float, int]:
        total_price = 0
        total_bonuses = 0
        items = (cart.items
                 .select_related('product')
                 .prefetch_related('freqbot__products')
                 .prefetch_related('product__filters__subfilters')
                 .prefetch_related('attributes__sub_filter')
                 .all()
                 )
        for cart_item in items.filter(product=None):
            total_bonuses = total_bonuses + cart_item.bonus_points()
            total_price = total_price + cart_item.price()

        for cart_item in items.filter(freqbot=None):
            total_bonuses = total_bonuses + cart_item.bonus_points()
            total_price = total_price + cart_item.price()
        return total_bonuses, total_price, cart.items.count()

    @staticmethod
    def finish_order(
            user: User,
            order: Order,
            total_price: float,
            bonuses: int,
            promo_code: PromoCode = None,
    ) -> None:
        user.bonus_points = user.bonus_points + bonuses
        user.save()
        if promo_code:
            total_price = make_sale(total_price, promo_code.discount)
            user.promo_codes.add(promo_code)
            for item in order.items.all():
                item: OrderItem
                item.cost = make_sale(item.cost, promo_code.discount)
                item.save()
        if user.subscribe_sale_active:
            setting = Setting.objects.first()
            total_price = make_sale(total_price, setting.subscribe_sale)
            for item in order.items.all():
                item: OrderItem
                item.cost = make_sale(item.cost, setting.subscribe_sale)
                item.save()
        order.total_price = total_price
        order.save()
        change_order_status.delay(order_id=order.id)

    def create_order(self, request: HttpRequest, code: str | None = None) \
            -> OrderOutSchema:
        """
        Create order for user.

        :param request: HttpRequest
        :param code: promo code for order if exists
        """
        cart = self.get_my_cart(request=request)
        if cart.items.count() <= 0:
            raise HttpError(400, _("Your cart is empty"))
        auth_user = False

        if random.choice([True, False, False]):
            raise HttpError(400, _(""
                                   "Here is a text that will "
                                   "describe the possible "
                                   "cause of the error and options "
                                   "for solving it."))

        user = request.auth
        if isinstance(user, User):
            auth_user = True
            promo_code = None
            if code:
                promo_code = self.check_promo_code(code=code, user=user)
            total_price = 0
            total_bonuses = 0
            order = Order.objects.create(
                status="IN PROGRESS", user_id=user.id, number=self.create_number(), total_price=0
            )
            for cart_item in (cart.items
                              .select_related('freqbot')
                              .prefetch_related('attributes__sub_filter',
                                                'freqbot__products')
                              .filter(product=None)):
                OrderItem.objects.create(
                    order=order, freqbot=cart_item.freqbot,
                    quantity=cart_item.quantity, cost=cart_item.price()
                )
                total_bonuses = total_bonuses + cart_item.bonus_points()
                total_price = total_price + cart_item.price()
            for cart_item in (cart.items
                              .select_related('product')
                              .prefetch_related('attributes__sub_filter__filter')
                              .filter(freqbot=None)):

                order_item = OrderItem.objects.create(
                    order=order, product=cart_item.product,
                    quantity=cart_item.quantity, cost=cart_item.price()
                )
                for attr in cart_item.attributes.all():
                    OrderItemAttribute.objects.create(
                        title_en=attr.sub_filter.filter.title_en,
                        title_uk=attr.sub_filter.filter.title_uk,
                        subtitle_en=attr.sub_filter.title_en,
                        subtitle_uk=attr.sub_filter.title_uk,
                        subfilter_id=attr.sub_filter.id,
                        order_item=order_item,
                    )
                total_bonuses = total_bonuses + cart_item.bonus_points()
                total_price = total_price + cart_item.price()

            order.total_price = total_price
            order.total_bonuses = total_bonuses
            order.save()
            self.finish_order(
                user=user, order=order, promo_code=promo_code,
                total_price=total_price, bonuses=total_bonuses
            )
            # clean user's cart
            cart.items.all().delete()
            if user.subscribe_sale_active:
                user.subscribe_sale_active = False
                user.save()
        cart.items.all().delete()
        return OrderOutSchema(message=_("Order issued successfully"),
                              auth_user=auth_user)

    @staticmethod
    def get_my_orders(user_id: int, page: int, page_size: int) -> dict:
        """
        Get user's orders by user's id.
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :param user_id: user id
        :return: paginated orders
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No User matches "
                              "the given query."))
        # Order.objects.prefetch_related('items__product__filters')
        orders = (Order.objects
                  .prefetch_related('items__attributes__subfilter__filter')
                  .prefetch_related('items__product__filters')
                  .prefetch_related('items__freqbot')
                  .filter(user=user))
        # orders = user.order_set.all()
        return paginate(items=orders, page=page, page_size=page_size)

    @staticmethod
    def get_order_detail(user_id: int, number: int) -> QuerySet:
        """
        Get user's order by order's number.
        :param number: number of order
        :param user_id: user id
        :return: paginated orders
        """
        try:
            user = User.objects.get(id=user_id)
            order = (Order.objects
                     .prefetch_related("items__attributes")
                     .prefetch_related("items__freqbot")
                     .prefetch_related("items__product__catalog_page__game")
                     .get(user=user, number=number))

        except User.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No User matches "
                              "the given query."))
        except Order.DoesNotExist:
            raise HttpError(404, _("Not Found: No Order matches "
                                   "the given query."))
        return order.items.all()

    def repeat_order(self, user: User, number: str) -> MessageOutSchema:
        """
        Repeat user's order by order id.
        :param user: User model instance
        :param number: order's number
        :return: message that repeated or not
        """

        try:
            order = (Order.objects
                     .prefetch_related("items__attributes__subfilter__filter__product")
                     .prefetch_related("items__product",
                                       "items__freqbot")
                     .get(number=number))
        except Order.DoesNotExist:
            raise HttpError(404, _("Not Found: No Order matches" " the given query."))

        for item in order.items.all():
            condition1 = item.freqbot and item.freqbot.is_deleted
            condition2 = item.product and item.product.is_deleted
            if condition1 or condition2:
                raise HttpError(404, _("Cannot repeat order, "
                                       "some products does "
                                       "not exists nowadays"))
            for attr in item.attributes.all():
                if attr.subfilter is None or attr.subfilter.filter.product.id != item.product.id:
                    raise HttpError(404, _("Cannot repeat order, "
                                           "some products does "
                                           "not exists nowadays"))

        kwargs = model_to_dict(
            order,
            exclude=[
                "id",
                "user",
                "status",
                "number",
            ],
        )

        new_order = Order.objects.create(**kwargs,
                                         user=user,
                                         status="IN PROGRESS",
                                         number=self.create_number())
        total_bonuses = 0
        total_price = 0
        for item in order.items.all():
            kwargs = model_to_dict(item, exclude=["id",
                                                  "order",
                                                  "freqbot",
                                                  "date_created",
                                                  "product"])
            new_order_item = OrderItem.objects.create(
                **kwargs,
                order=new_order,
                product=item.product,
                freqbot=item.freqbot,
            )
            for attr in item.attributes.all():
                kwargs = model_to_dict(attr, exclude=["id",
                                                      "subfilter",
                                                      "order_item"])
                OrderItemAttribute.objects.create(
                    **kwargs,
                    subfilter=attr.subfilter,
                    order_item=new_order_item,
                )
            new_order_item.cost = new_order_item.price()
            new_order_item.save()
            total_price = total_price + new_order_item.price()
            total_bonuses = total_bonuses + new_order_item.bonus_points()
        self.finish_order(user=user, order=new_order, promo_code=None,
                          total_price=total_price, bonuses=total_bonuses)
        return MessageOutSchema(message=_("Order repeated successfully"))

    @staticmethod
    def check_promo_code(code: str, user: User) -> PromoCode:
        """
        Checks promo code
        used in cart page in the site
        :param user: current user
        :param code: promo code
        :return: dict which contains parameters for pagination
        :rtype: dict
        """

        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            raise HttpError(404, _("Not Found: No PromoCode matches "
                                   "the given query."))
        current_datetime = timezone.now().date()
        if not (promo_code.until_date >=
                current_datetime >=
                promo_code.from_date):
            raise HttpError(403, _("Promo code has been expired"))
        if user.promo_codes.filter(code=code).exists():
            raise HttpError(410, _("Promo code has been already used"))

        return promo_code
