from ninja import ModelSchema, Schema
from typing import List

from pydantic import EmailStr

from src.users.models import User


class UserOutSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class SubscribeInSchema(Schema):
    email: EmailStr


class RegisterSchema(Schema):
    email: EmailStr
    password: str
    notify_me: bool
