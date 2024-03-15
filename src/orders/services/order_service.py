# -*- coding: utf-8 -*-
"""
    Module contains class for managing orders on site
"""
from django.contrib.auth import get_user_model
# -*- coding: utf-8 -*-
from django.db.models import QuerySet
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, get_list_or_404

from ninja.errors import HttpError

from src.main.models import OrderItem
from src.main.schemas import OrderOutSchema
from src.main.services.main_service import MainService
from src.orders.models import Cart, CartItem, Order
from src.orders.schemas import CreateOrderInSchema
from src.products.utils import make_sale
from src.users.schemas import MessageOutSchema

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
            cart, status = (Cart.objects.prefetch_related('items')
                            .get_or_create(user=user))
        else:
            cart, status = (Cart.objects.prefetch_related('items')
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
        item = get_object_or_404(CartItem, cart_id=cart.id, id=item_id)
        item.delete()
        return MessageOutSchema(message='Cart items has been deleted successfully')

    def create_order(self, user: User | str, body: CreateOrderInSchema) -> OrderOutSchema:
        """
        Create order for user.

        :param body: all cart item's for buying
        :param user: User model instance or session key
        """
        cart = self.get_my_cart(user=user)
        list_ids = cart.items.values_list('id', flat=True)
        for item_id in body.items:
            if item_id in list_ids:
                continue
            raise HttpError(404, f'Cart item with id {item_id} not found')

        # if random.choice([True, False]):
        if isinstance(user, User):
            promo_code = None
            if body.promo_code:
                promo_code = (MainService.
                              check_promo_code(code=body.promo_code,
                                               user=user))

            order = Order.objects.create(status='completed',
                                         user_id=user.id,
                                         total_price=0)
            total_price = 0
            total_bonuses = 0
            instances = get_list_or_404(CartItem, id__in=body.items)
            for inst in instances:
                OrderItem.objects.create(order_id=order.id,
                                         title=inst.product.title,
                                         subtitle=inst.product.subtitle,
                                         product_id=inst.product.id)
                total_price = total_price + inst.price()
                bonuses = inst.product.bonus_points * inst.quantity
                total_bonuses = total_bonuses + bonuses
            user.bonus_points = user.bonus_points + total_bonuses
            user.save()
            if promo_code:
                order.total_price = make_sale(total_price, promo_code.discount)
                user.promo_codes.add(promo_code)
            else:
                order.total_price = total_price
            order.save()

            return OrderOutSchema(message='Order issued successfully',
                                  auth_user=True)
        else:
            return OrderOutSchema(message='Order issued successfully',
                                  auth_user=False)

    @staticmethod
    def get_my_orders(user_id: int) -> QuerySet:
        """
        Get user's orders by user's id.
        :param user_id: user id
        :return: User model instance
        """
        user = get_object_or_404(User, id=user_id)
        orders = user.order_set.all()
        return orders

    @staticmethod
    def repeat_order(user: User, order_id: str) -> Order:
        """
        Repeat user's order by order id.
        :param user: User model instance
        :param order_id: order's id which have to repeat
        :return: message that repeated or not
        """
        order = get_object_or_404(Order, id=order_id, user=user)
        for item in order.items.values_list('product_id', flat=True):
            if item is None:
                raise HttpError(404, 'Cannot repeat order, '
                                     'some products are '
                                     'not exists nowadays ☹')
        kwargs = model_to_dict(order, exclude=['id', 'user'])
        new_order = Order.objects.create(**kwargs, user=user)
        total_bonuses = 0
        for item in order.items.all():
            kwargs = model_to_dict(item, exclude=['id',
                                                  'order',
                                                  'product'])
            OrderItem.objects.create(**kwargs,
                                     order=new_order,
                                     product=item.product)
            total_bonuses = total_bonuses + item.product.bonus_points
        user.bonus_points = user.bonus_points + total_bonuses
        user.save()
        return new_order
