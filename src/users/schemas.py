# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "users".

implement logic for encoding and decoding data into python
object and json
"""
from enum import Enum
from typing import List

from allauth.socialaccount.models import SocialAccount
from ninja import ModelSchema, Schema
from pydantic import EmailStr

from config.settings import ABSOLUTE_URL
from src.main.models import OrderItem, OrderItemAttribute
from src.orders.models import Order
from src.users.models import User, Character

from django.utils.translation import gettext as _


class Error(Schema):
    message: str


class SocialAccountSchema(ModelSchema):
    class Meta:
        model = SocialAccount
        fields = (
            "id",
            "provider",
            "uid",
            "last_login",
            "date_joined",
        )


class SocialLoginSchema(Schema):
    access_token: str



class UserOutSchema(ModelSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to return user's
    personal data(except password) to client side
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'payment_method', 'communication',
                  'notify_me', 'bonus_points', 'subscribe_sale_active']


class UserUpdatedSchema(ModelSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to return user's
    personal data(except password) to client side
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'payment_method', 'communication',
                  'notify_me', ]


class CharacterOutSchema(ModelSchema):
    """
    Pydantic schema for Characters.

    Purpose of this schema to return user's
    characters
    """

    class Meta:
        model = Character
        fields = '__all__'
        exclude = ['user', 'date_published']


class Faction(str, Enum):
    Alliance = 'Alliance'
    Horde = 'Horde'


class ClassAndSpec(str, Enum):
    Warrior = "Warrior"
    Paladin = "Paladin"
    Hunter = "Hunter"
    Rogue = "Rogue"
    Priest = "Priest"
    Shaman = "Shaman"
    Mage = "Mage"
    Warlock = "Warlock"
    Monk = "Monk"
    Druid = "Druid"


class CharacterInSchema(ModelSchema):
    """
    Pydantic schema for Characters.

    Purpose of this schema to update user's
    characters
    """
    battle_tag: str = None
    name: str = None
    faction: Faction = None
    additional_info: str = None
    class_and_spec: ClassAndSpec = None
    realm: str = None

    class Meta:
        model = Character
        fields = '__all__'
        exclude = ['id', 'user', 'date_published']


class PaymentMethod(str, Enum):
    PayPal = "PayPal"
    Visa = "Visa"
    MasterCard = "MasterCard"
    AmericanExpress = "AmericanExpress"


class CommunicationMethod(str, Enum):
    Telegram = "Telegram"
    Viber = "Viber"
    Discord = "Discord"
    Skype = "Skype"
    Facebook = "Facebook"
    WhatsApp = "WhatsApp"


class UserInSchema(Schema):
    """
    Pydantic schema for User.

    Purpose of this schema to return user's
    personal data(except password) to client side
    """
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    payment_method: PaymentMethod | None = None
    communication: CommunicationMethod | None = None
    notify_me: bool | None = None


class MessageOutSchema(Schema):
    """
    Pydantic schema for return message to client side.

    Purpose of this schema just say that operation
    has been successful
    """

    message: str | None


class RegisterSchema(Schema):
    """
    Pydantic schema for registration new users in the site.

    Purpose of this schema to give data in endpoint for registration
    """

    email: EmailStr
    password: str
    notify_me: bool


class EmailSchema(Schema):
    """
    Pydantic schema for subscribe users to news in the site.

    Purpose of this schema to give data in endpoint for subscribing
    """
    email: EmailStr


class OrderItemAttributeSchema(ModelSchema):
    """
    Pydantic schema for order item attributes.

    Purpose of this schema to update user's
    characters
    """

    class Meta:
        model = OrderItemAttribute
        fields = ['title', 'price']


class OrdersItemSchema(ModelSchema):
    card_img: str | None = None
    card_img_alt: str | None = None
    game_logo: str | None = None
    game_logo_alt: str | None = None
    title: str | None = None
    subtitle: str | None = None
    attributes: List[OrderItemAttributeSchema] = []

    @staticmethod
    def resolve_card_img(obj):
        if obj.product is None:
            return None
        return ABSOLUTE_URL + obj.product.card_img.url

    @staticmethod
    def resolve_game_logo(obj):
        if obj.product is None:
            return None
        return (ABSOLUTE_URL +
                obj.product.catalog_page.game.logo_product.url)

    @staticmethod
    def resolve_game_logo_alt(obj):
        if obj.product is None:
            return None
        return obj.product.catalog_page.game.logo_product_alt

    @staticmethod
    def resolve_card_img_alt(obj):
        if obj.product is None:
            return None
        return obj.product.card_img_alt

    @staticmethod
    def resolve_title(obj):
        if obj.product is None:
            return None
        return obj.product.title

    @staticmethod
    def resolve_subtitle(obj):
        if obj.product is None:
            return None
        return obj.product.subtitle

    # @staticmethod
    # def resolve_subtitle(obj):
    #     if obj.product is None:
    #         return None
    #     return obj.product.subtitle

    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['order', 'product', 'id']


class CabinetOrdersSchema(ModelSchema):
    """
    Pydantic schema for return orders to cabinet.

    """
    items: list[OrdersItemSchema]
    repeat_btn: bool
    status: str

    @staticmethod
    def resolve_status(obj):
        return _(obj.status)

    @staticmethod
    def resolve_repeat_btn(obj):
        for item in obj.items.all():
            if item.product.is_deleted:
                return False

            for attr in item.attributes.all():
                if (attr.subfilter is None or
                        attr.subfilter.filter.product.id
                        != item.product.id):
                    return False
        return True

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user', 'freqbot', 'id']


class ConfirmationSchema(Schema):
    """
    Pydantic schema for confirm operations in the site.

    Purpose of this schema to give data in confirms endpoints
    """
    uidb64: str
    token: str


class ChangePasswordSchema(Schema):
    """
    Pydantic schema for change password in the site.

    Purpose of this schema to give data in endpoint change-password
    """
    uidb64: str
    token: str
    password1: str
    password2: str
