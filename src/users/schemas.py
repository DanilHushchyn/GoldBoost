# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "users"
implement logic for encoding and decoding data into python
object and json
"""
from ninja import ModelSchema, Schema
from pydantic import EmailStr

from src.users.models import User


class UserOutSchema(ModelSchema):
    """
    Pydantic schema for User.
    Purpose of this schema to return user's
    personal data(except password) to client side
    """
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


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
