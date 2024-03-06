# -*- coding: utf-8 -*-
"""
Module contain classes Managers for models in app products
These Managers implement most frequently used methods
for selecting data in models
"""
from django.db import models


class ProductManager(models.Manager):
    """
    A Manager class for managing products.
    This class provides methods for ordering and filtering products with db queries.
    """

    def hot_all(self, game_id=None):
        if game_id:
            objects = (
                self.get_queryset()
                .select_related("catalog_page__game")
                .filter(tag__name__iexact="hot", catalog_page__game=game_id)
            )
        else:
            objects = self.get_queryset().select_related("catalog_page__game").filter(tag__name__iexact="hot")
        return objects

    def bestsellers(self):
        objects = self.get_queryset().order_by("-bought_count")
        return objects
