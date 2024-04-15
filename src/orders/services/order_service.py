# -*- coding: utf-8 -*-
"""
    Module contains class for managing orders on site
"""
import random

from django.contrib.auth import get_user_model
# -*- coding: utf-8 -*-
from django.db.models import QuerySet
from django.forms import model_to_dict

from ninja.errors import HttpError

from src.main.models import OrderItem, PromoCode, OrderItemAttribute, Setting
from src.main.schemas import OrderOutSchema
from src.main.services.main_service import MainService
from src.orders.models import Cart, CartItem, Order
from src.orders.tasks import change_order_status
from src.products.utils import make_sale
from src.users.schemas import MessageOutSchema
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja.errors import HttpError

User = get_user_model()


class OrderService:
    """
    A service class for managing orders.

    This class provides methods for ordering, filtering,
    paginating and getting related entities of orders.
    """

    @staticmethod
    def get_my_cart(user: User | str) -> Cart:
        """
        Gets info for user's cart.

        :param user:
        :return: Cart model instance
        """
        if isinstance(user, User):
            cart, status = (Cart.objects.prefetch_related('items', 'items__attributes')
                            .get_or_create(user=user))
        else:
            cart, status = (Cart.objects.prefetch_related('items', 'items__attributes')
                            .get_or_create(session_key=user))
        return cart

    def delete_cart_item(self, user: User | str, item_id: int) -> MessageOutSchema:
        """
        Delete cart's item it's by id.

        :param item_id: cart's item id
        :param user:
        :return: Cart model instance
        """
        cart = self.get_my_cart(user=user)
        try:
            item = CartItem.objects.get(cart_id=cart.id, id=item_id)
        except CartItem.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No CartItem matches"
                              " the given query."))
        item.delete()
        return MessageOutSchema(message=_('Cart items has been deleted successfully'))

    @staticmethod
    def create_number():
        while True:
            num = random.randint(100_000_000, 999_999_999)
            if not Order.objects.filter(number=num).exists():
                break
        return num

    @staticmethod
    def finish_order(user: User, order: Order, total_price: float,
                     bonuses: int, promo_code: PromoCode = None, ) \
            -> None:
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

    def create_freq_order(self, user, cart_item: CartItem, promo_code: PromoCode = None):
        freq_order = Order.objects.create(status='IN PROGRESS',
                                          user_id=user.id,
                                          number=self.create_number(),
                                          freqbot=cart_item.freqbot,
                                          total_price=0)
        for item in cart_item.freqbot.products.all():
            order_item = OrderItem.objects.create(order_id=freq_order.id,
                                                  quantity=1,
                                                  product_id=item.id)
            order_item.cost = make_sale(order_item.price(),
                                        cart_item.freqbot.discount)
            order_item.save()
        total_price = cart_item.price()
        bonuses = cart_item.bonus_points()
        self.finish_order(user=user,
                          order=freq_order,
                          promo_code=promo_code,
                          total_price=total_price,
                          bonuses=bonuses)

    def create_ordinary_order(self, user, cart: Cart,
                              promo_code: PromoCode = None):
        total_price = 0
        total_bonuses = 0
        order = Order.objects.create(status='IN PROGRESS',
                                     user_id=user.id,
                                     number=self.create_number(),
                                     total_price=0)
        for cart_item in cart.items.exclude(product=None):
            order_item = OrderItem.objects.create(order_id=order.id,
                                                  quantity=cart_item.quantity,
                                                  product_id=cart_item.product.id)
            for attr in cart_item.attributes.all():
                OrderItemAttribute.objects.create(
                    title_en=attr.sub_filter.title_en,
                    title_uk=attr.sub_filter.title_uk,
                    price=attr.sub_filter.price,
                    subfilter_id=attr.sub_filter.id,
                    order_item=order_item,
                )
            order_item.cost = order_item.price()
            order_item.save()

            # cart_item.attributes.all()
            total_price = total_price + cart_item.price()
            bonuses = cart_item.bonus_points()
            total_bonuses = total_bonuses + bonuses
        self.finish_order(user=user,
                          order=order,
                          promo_code=promo_code,
                          total_price=total_price,
                          bonuses=total_bonuses)

    def create_order(self, user: User | str,
                     code: str | None = None) \
            -> OrderOutSchema:
        """
        Create order for user.

        :param code: promo code for order if exists
        :param user: User model instance or session key
        """
        cart = self.get_my_cart(user=user)
        if cart.items.count() <= 0:
            raise HttpError(400, _('Your cart is empty'))
        auth_user = False
        if isinstance(user, User):
            auth_user = True
            promo_code = None
            if code:
                promo_code = self.check_promo_code(code=code,
                                                   user=user)
            for cart_item in cart.items.filter(product=None):
                self.create_freq_order(user=user,
                                       cart_item=cart_item,
                                       promo_code=promo_code)

            if cart.items.exclude(product=None).exists():
                self.create_ordinary_order(user=user,
                                           cart=cart,
                                           promo_code=promo_code)
            # clean user's cart
            # cart.items.all().delete()
            if user.subscribe_sale_active:
                user.subscribe_sale_active = False
                user.save()
        return OrderOutSchema(message=_('Order issued successfully'),
                              auth_user=auth_user)

    @staticmethod
    def get_my_orders(user_id: int) -> QuerySet:
        """
        Get user's orders by user's id.
        :param user_id: user id
        :return: User model instance
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No User matches"
                              " the given query."))
        orders = user.order_set.all()
        return orders

    def repeat_order(self, user: User, number: str) -> MessageOutSchema:
        """
        Repeat user's order by order id.
        :param user: User model instance
        :param number: order's number
        :return: message that repeated or not
        """

        try:
            order = (Order.objects
                     .prefetch_related('items', 'items__attributes')
                     .get(number=number)
                     )
        except Order.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No Order matches"
                              " the given query."))

        for item in order.items.all():
            if item.product.is_deleted:
                raise HttpError(404, _('Cannot repeat order, '
                                       'some products does '
                                       'not exists nowadays'))
            for attr in item.attributes.all():
                if (attr.subfilter is None or
                        attr.subfilter.filter.product.id
                        != item.product.id):
                    raise HttpError(404, _('Cannot repeat order, '
                                           'some products does '
                                           'not exists nowadays'))

        kwargs = model_to_dict(order, exclude=['id',
                                               'user',
                                               'status',
                                               'number',
                                               'freqbot'])

        new_order = Order.objects.create(**kwargs,
                                         user=user,
                                         freqbot=order.freqbot,
                                         status='IN PROGRESS',
                                         number=self.create_number())
        total_bonuses = 0
        total_price = 0
        for item in order.items.all():
            kwargs = model_to_dict(item, exclude=['id',
                                                  'order',
                                                  'product'])
            new_order_item = OrderItem.objects.create(**kwargs,
                                                      order_id=new_order.id,
                                                      product=item.product)
            for attr in item.attributes.all():
                kwargs = model_to_dict(attr, exclude=['id', 'price', 'subfilter', 'order_item'])
                price = attr.subfilter.price
                OrderItemAttribute.objects.create(
                    **kwargs,
                    price=price,
                    subfilter=attr.subfilter,
                    order_item=new_order_item,
                )
            new_order_item.cost = new_order_item.price()
            new_order_item.save()

            total_price = total_price + item.price()
            total_bonuses = total_bonuses + item.bonus_points()
        if new_order.freqbot:
            discount = new_order.freqbot.discount
            for item in new_order.items.all():
                item.cost = make_sale(item.cost, discount)
                item.save()
            total_price = make_sale(total_price, discount)
        self.finish_order(user=user,
                          order=new_order,
                          promo_code=None,
                          total_price=total_price,
                          bonuses=total_bonuses)
        return MessageOutSchema(message=_('Order repeated successfully'))

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
            raise HttpError(404,
                            _("Not Found: No PromoCode matches"
                              " the given query."))
        current_datetime = timezone.now().date()
        if not (
                promo_code.until_date >=
                current_datetime >=
                promo_code.from_date
        ):
            raise HttpError(403, _("Promo code has been expired"))
        if user.promo_codes.filter(code=code).exists():
            raise HttpError(410, _("Promo code has been already used"))

        return promo_code
