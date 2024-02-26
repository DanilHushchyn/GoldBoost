from django.db import models

# Create your models here.
from django.db import models

from src.games.models import CatalogPage, Tab
from src.website.utils import get_timestamp_path


class Product(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_timestamp_path, null=True)
    description = models.TextField()
    price = models.FloatField()
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('range', 'Range')
    ]
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES)
    bonus_points = models.IntegerField(default=0)
    sale = models.BooleanField()
    sale_percent = models.PositiveSmallIntegerField()
    sale_from = models.DateTimeField()
    sale_until = models.DateTimeField()
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, null=True)
    filter = models.ForeignKey('Filter', on_delete=models.CASCADE, null=True)
    runs = models.BooleanField()
    price_per_run = models.FloatField()
    bought_count = models.IntegerField()
    catalog_page = models.ForeignKey(CatalogPage, on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tags'
        verbose_name_plural = 'Tags'


class Filter(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('Select', 'Select'), ('Radio', 'Radio'), ('CheckBox', 'CheckBox')])

    class Meta:
        verbose_name = 'Filters'
        verbose_name_plural = 'Filters'


class SubFilter(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    filter = models.ForeignKey("Filter", on_delete=models.CASCADE, null=True)
