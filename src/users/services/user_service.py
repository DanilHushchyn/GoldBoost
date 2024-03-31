# -*- coding: utf-8 -*-
"""
    Module contains class for managing users data in the site.

"""
from django.db import IntegrityError
from django.db.models import QuerySet
from ninja.errors import HttpError

from src.users.models import Character, Subscriber, User
from src.users.schemas import CharacterInSchema, MessageOutSchema, UserInSchema, EmailSchema
from django.utils.translation import gettext as _


class UserService:
    """
    A service class for managing users.
    """

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Get user personal data by id.

        :param user_id: user id
        :return: User model instance
        """

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No User matches"
                              " the given query."))
        return user

    @staticmethod
    def update_my_profile(user_id: int, user_body: UserInSchema) -> User:
        """
        Get user personal data by id.

        :param user_body: here fields that have to be updated
        :param user_id: user id
        :return: User model instance
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No User matches"
                              " the given query."))
        for key, value in user_body.dict().items():
            if key == 'notify_me' and value and user.subscribe_sale_active is None:
                user.subscribe_sale_active = True
            if value is not None:
                setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def get_my_profile(user_id: int) -> User:
        """
        Get user personal data by id.

        :param user_id: user id
        :return: User model instance
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No User matches"
                              " the given query."))
        return user

    @staticmethod
    def get_my_characters(user_id: int) -> QuerySet:
        """
        Get user's characters data.

        :param user_id: user id
        :return: User model instance
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No User matches"
                              " the given query."))
        return user.character_set.all()

    @staticmethod
    def update_character_by_id(character_id: int, character: CharacterInSchema) -> Character:
        """
        Get user's characters data.

        :param character_id:
        :param character:
        :return: User model instance
        """
        try:
            obj = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No Character matches"
                              " the given query."))
        for key, value in character.dict().items():
            if value:
                setattr(obj, key, value)
        obj.save()
        return obj

    @staticmethod
    def delete_character_by_id(character_id: int) -> MessageOutSchema:
        """
        Delete user's character by id.

        :param character_id:
        :return: User model instance
        """
        try:
            obj = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            raise HttpError(404,
                            _("Not Found: No Character matches"
                              " the given query."))
        obj.delete()
        return MessageOutSchema(message=_("Character deleted successfully"))

    @staticmethod
    def create_character(user_id: int) -> Character:
        """
        Create user's character.

        :return: Character model instance
        """
        if Character.objects.filter(user_id=user_id).count() >= 3:
            raise HttpError(409,
                            _("Not more than 3 characters "
                              "are possible to create"))
        character = Character.objects.create(user_id=user_id)
        return character

    @staticmethod
    def subscribe(body: EmailSchema) -> MessageOutSchema:
        """
        Subscribe user's email to get news.

        :param body: user's email
        :return: message that user subscribed
        """
        try:
            Subscriber.objects.create(email=body.email)
        except IntegrityError:
            raise HttpError(409,
                            _("This email has been already subscribed"))
        return MessageOutSchema(message=_("You are successfully subscribed"))
