from django.db import models
from meta.models import ModelMeta

from src.website.utils import get_timestamp_path

from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    logo_filter = models.ImageField(upload_to=get_timestamp_path, null=True)
    logo_product = models.ImageField(upload_to=get_timestamp_path, null=True)
    logo_filter_alt = models.CharField(max_length=255, null=True)
    logo_product_alt = models.CharField(max_length=255, null=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'Games'
        verbose_name_plural = 'Games'


class CatalogPage(ModelMeta, models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    title = models.CharField()
    description = models.TextField()
    tab = models.ForeignKey('Tab', on_delete=models.SET_NULL, blank=True, null=True, related_query_name='tab_content')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=True, related_query_name='game',
                             related_name='catalog_pages')
    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    _metadata = {
        'title': 'title',
        'description': 'description',
    }

    class Meta:
        verbose_name = 'Catalog Page'
        verbose_name_plural = 'Catalog Pages'


class WorthLookCarouselItem(models.Model):
    image = models.ImageField(upload_to=get_timestamp_path, null=True)
    image_alt = models.CharField(max_length=255, null=True)
    title = models.CharField()
    link = models.URLField()
    catalog_page = models.ForeignKey('CatalogPage', on_delete=models.CASCADE, related_name='worth_items', null=True)

    class Meta:
        verbose_name = 'Worth look carousel'
        verbose_name_plural = 'Worth look carousel'


class TabItem(models.Model):
    title = models.CharField()
    content = models.TextField()
    order = models.PositiveIntegerField(null=True)
    tab = models.ForeignKey('Tab', on_delete=models.CASCADE, related_name='tab_items', null=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Tab Item'
        verbose_name_plural = 'Tab Items'


class Tab(models.Model):
    class Meta:
        verbose_name = 'Tab'
        verbose_name_plural = 'Tabs'


class Calendar(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Calendars'
        verbose_name_plural = 'Calendars'


class CalendarItem(models.Model):
    date = models.DateField()
    team1_img = models.ImageField()
    team1_img_alt = models.CharField(max_length=255, null=True)
    team1_from = models.TimeField()
    team1_until = models.TimeField()
    team2_img = models.ImageField()
    team2_img_alt = models.CharField(max_length=255, null=True)
    team2_from = models.TimeField()
    team2_until = models.TimeField()
    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE, null=True)
