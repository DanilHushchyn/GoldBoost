# -*- coding: utf-8 -*-
"""
    Module contains class for managing users data in the site
"""

from django.shortcuts import get_object_or_404

from src.users.models import User


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
