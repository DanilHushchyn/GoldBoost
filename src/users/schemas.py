# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "users"
implement logic for encoding and decoding data into python
object and json
"""
from enum import Enum

from ninja import ModelSchema, Schema
from pydantic import EmailStr

from config.settings import ABSOLUTE_URL
from src.main.models import OrderItem
from src.orders.models import Order
from src.users.models import User, Character


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
                  'notify_me', 'bonus_points']


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


class OrdersItemSchema(ModelSchema):
    card_img: str | None = None
    game_logo: str | None = None

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

    @staticmethod
    def resolve_repeat_btn(obj):
        for item in obj.items.values_list('product_id', flat=True):
            if item is None:
                return False
        return True

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user']
