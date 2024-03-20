# -*- coding: utf-8 -*-
"""
    Module contains class for managing users data in the site.

"""
from django.db import IntegrityError
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

from src.users.models import Character, Subscriber, User
from src.users.schemas import CharacterInSchema, MessageOutSchema, UserInSchema, UserOutSchema


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

        user = get_object_or_404(User, id=user_id)
        return user

    @staticmethod
    def update_my_profile(user_id: int, user_body: UserInSchema) -> User:
        """
        Get user personal data by id.

        :param user_body: here fields that have to be updated
        :param user_id: user id
        :return: User model instance
        """
        user = get_object_or_404(User, id=user_id)
        for key, value in user_body.dict().items():
            if value:
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
        user = get_object_or_404(User, id=user_id)
        return user

    @staticmethod
    def get_my_characters(user_id: int) -> QuerySet:
        """
        Get user's characters data.

        :param user_id: user id
        :return: User model instance
        """
        user = get_object_or_404(User, id=user_id)

        return user.character_set.all()

    @staticmethod
    def update_character_by_id(character_id: int, character: CharacterInSchema) -> Character:
        """
        Get user's characters data.

        :param character_id:
        :param character:
        :return: User model instance
        """
        obj = get_object_or_404(Character, id=character_id)
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
        obj = get_object_or_404(Character, id=character_id)
        obj.delete()
        return MessageOutSchema(message="Character deleted successfully")

    @staticmethod
    def create_character(user_id: int) -> Character:
        """
        Create user's character.

        :return: Character model instance
        """
        if Character.objects.filter(user_id=user_id).count() >= 3:
            raise HttpError(409,
                            "Not more than 3 characters "
                            "are possible to create ☹")
        character = Character.objects.create(user_id=user_id)
        return character

    @staticmethod
    def subscribe(email: str) -> MessageOutSchema:
        """
        Subscribe user's email to get news.

        :param email: user's email
        :return: message that user subscribed
        """
        try:
            Subscriber.objects.create(email=email)
        except IntegrityError:
            raise HttpError(409,
                            "This email has been already subscribed ☹")
        return MessageOutSchema(message="You are successfully subscribed")
