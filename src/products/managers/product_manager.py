from django.db import models
from django.db.models import F, Sum
from django.db.models.functions.text import Concat
from django.forms import CharField
from django.db.models import Value, CharField, F, Sum


class ProductManager(models.Manager):

    def hot_all(self, game_id=None):
        if game_id:
            objects = self.get_queryset().filter(tag__name__iexact='hot', catalog_page__game=game_id)
        else:
            objects = self.get_queryset().filter(tag__name__iexact='hot')
        for obj in objects:
            obj.game_logo = obj.catalog_page.game.logo_product.url
        return objects

    def bestsellers(self):
        objects = self.get_queryset().order_by('-bought_count')
        for obj in objects:
            obj.game_logo = obj.catalog_page.game.logo_product.url
        return objects
