# -*- coding: utf-8 -*-
"""
    In this module described models for application games.

    The main model here is Main and also initialized related to it models
"""
from django.db import models
from meta.models import ModelMeta

from src.games.managers.catalog_manager import CatalogPageManager
from src.games.managers.game_manager import GameManager
from src.products.utils import get_timestamp_path


class Game(models.Model):
    """
    Model for storing data about all games in the site.

    """

    name = models.CharField(max_length=255)
    logo_filter = models.ImageField(upload_to=get_timestamp_path,
                                    null=True)
    logo_product = models.ImageField(upload_to=get_timestamp_path,
                                     null=True)
    logo_filter_alt = models.CharField(max_length=255, null=True)
    logo_product_alt = models.CharField(max_length=255, null=True)
    order = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)
    objects = GameManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name = "Games"
        verbose_name_plural = "Games"
        db_table = 'games'


class CatalogPage(ModelMeta, models.Model):
    """
    Model for storing data about related to game page in catalog.

    """

    parent = models.ForeignKey("self", on_delete=models.SET_NULL,
                               blank=True, null=True,
                               related_name="items")
    title = models.CharField()
    description = models.TextField()
    game = models.ForeignKey(
        "Game", on_delete=models.SET_NULL,
        null=True, related_query_name="game",
        related_name="catalog_pages"
    )
    calendar = models.ForeignKey("Calendar",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    worth_look = models.ForeignKey("WorthLook",
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    order = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)
    objects = CatalogPageManager()

    def __str__(self):
        return self.title

    _metadata = {
        "title": "title",
        "description": "description",
    }

    class Meta:
        ordering = ["order"]
        verbose_name = "Catalog Page"
        verbose_name_plural = "Catalog Pages"
        db_table = 'catalog_pages'


class CatalogTabs(models.Model):
    """
    Model for storing tabs for model CatalogPage.

    which admin want to emphasize
    """

    title = models.CharField()
    content = models.TextField()
    order = models.PositiveIntegerField(null=True)
    catalog = models.ForeignKey("CatalogPage",
                                on_delete=models.CASCADE,
                                null=True, related_name='tabs')

    class Meta:
        ordering = ['order', ]
        verbose_name = "Catalog Tab"
        verbose_name_plural = "Catalog Tabs"
        db_table = 'catalog_tabs'


class WorthLook(models.Model):
    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Worth look"
        verbose_name_plural = "Worth look"
        db_table = 'worth_look'


class WorthLookItem(models.Model):
    """
    Related to CatalogPage models.

    implements section in the site with
    links to others pages of catalog
    """

    image = models.ImageField(upload_to=get_timestamp_path, null=True)
    image_alt = models.CharField(max_length=255, null=True)
    catalog_page = models.ForeignKey("CatalogPage",
                                     on_delete=models.CASCADE, null=True)
    carousel = models.ForeignKey("WorthLook",
                                 on_delete=models.CASCADE,
                                 related_name='items', null=True)

    def __str__(self):
        return self.catalog_page.title

    class Meta:
        verbose_name = "Worth look item"
        verbose_name_plural = "Worth look items"
        db_table = 'worth_look_items'


class Calendar(models.Model):
    """
    Model helps make calendar in the site.

    This model related to CatalogPage
    """
    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Calendar"
        verbose_name_plural = "Calendars"
        db_table = 'calendars'


class CalendarBlock(models.Model):
    """
    Model helps to make sum.

    multiple calendar events in one block
    """

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    calendar = models.ForeignKey("Calendar",
                                 on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Calendar Block"
        verbose_name_plural = "Calendar Blocks"
        db_table = 'calendar_blocks'


class CalendarBlockItem(models.Model):
    """
    Model is storing specific event in calendar.
    """

    date = models.DateField()
    # team1_img = models.ImageField()
    # team1_img_alt = models.CharField(max_length=255, null=True)
    team1_from = models.TimeField()
    team1_until = models.TimeField()
    #     team2_img = models.ImageField()
    #     team2_img_alt = models.CharField(max_length=255, null=True)
    team2_from = models.TimeField()
    team2_until = models.TimeField()
    block = models.ForeignKey("CalendarBlock",
                              on_delete=models.CASCADE, null=True)
    team1 = models.ForeignKey("Team", related_query_name='team1',
                              related_name='calendars1',
                              on_delete=models.CASCADE, null=True)
    team2 = models.ForeignKey("Team", related_query_name='team2',
                              related_name='calendars2',
                              on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'calendar_block_items'


class Team(models.Model):
    """
    Model is storing specific event in calendar.
    """

    team_img = models.ImageField()
    team_img_alt = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.team_img_alt

    class Meta:
        db_table = 'teams'
