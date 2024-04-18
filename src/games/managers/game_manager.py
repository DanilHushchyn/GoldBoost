# -*- coding: utf-8 -*-
"""
Module contain classes Managers for models in app games.

These Managers implement most frequently used methods
for selecting data in models
"""
from django.db import models


class GameManager(models.Manager):
    """
    A Manager class for managing games.

    This class provides methods for ordering and filtering games with db queries.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
