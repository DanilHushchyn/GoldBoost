# -*- coding: utf-8 -*-
"""
Module contain classes Managers for models in app products.

These Managers implement most frequently used methods
for selecting data in models
"""
from django.db import models
from django.db.models import Prefetch, prefetch_related_objects


class ProductManager(models.Manager):
    """
    A Manager class for managing products.

    This class provides methods for ordering and filtering products with db queries.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get_history(self):
        return super().get_queryset()

    def hot_all(self, game_id: int = None):
        if game_id:
            objects = (
                self.get_queryset()
                .select_related("catalog_page__game", 'tag')
                .prefetch_related('filters__subfilters')
                .filter(tag_id=1,
                        catalog_page__game=game_id)
            )

        else:
            objects = (self.get_queryset()
                       .select_related("catalog_page__game", 'tag')
                       .prefetch_related('filters__subfilters')
                       .filter(tag_id=1))
        return objects

    def bestsellers(self):
        # from src.products.models import Filter, SubFilter
        # fs = Prefetch(
        #     "filters",
        #     queryset=Filter.objects.prefetch_related(
        #         Prefetch('subfilters', queryset=SubFilter.objects.all(),)
        #     ).all(),
        # )
        objects = (self.get_queryset()
                   .select_related('catalog_page__game', 'tag')
                   .prefetch_related('filters__subfilters')
                   .order_by("-bought_count")
                   )
        return objects


class FreqBoughtManager(models.Manager):
    """
    A Manager class for managing freqbots.

    This class provides methods for ordering and filtering products with db queries.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
