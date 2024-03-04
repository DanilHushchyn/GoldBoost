from datetime import timedelta, datetime
from django.utils import timezone

from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Max, Sum, Min

from src.games.models import CatalogPage, Tab
from src.products.managers.product_manager import ProductManager
from src.website.utils import get_timestamp_path


class Product(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_timestamp_path, null=True)
    image_alt = models.CharField(max_length=255,null=True)
    card_img = models.ImageField(upload_to=get_timestamp_path, null=True)
    card_img_alt = models.CharField(max_length=255,null=True)
    description = models.TextField()
    price = models.FloatField()
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('range', 'Range')
    ]
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES)
    bonus_points = models.IntegerField(default=0)
    sale_percent = models.PositiveSmallIntegerField(blank=True, null=True)
    sale_from = models.DateTimeField(blank=True, null=True)
    sale_until = models.DateTimeField(blank=True, null=True)
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, null=True, blank=True)
    runs = models.BooleanField()
    price_per_run = models.FloatField(null=True, blank=True)
    bought_count = models.IntegerField(default=0)
    catalog_page = models.ForeignKey(CatalogPage, on_delete=models.CASCADE, related_name='products', null=True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def price_to(self):
        price_to = self.price
        if self.filters.count():
            for item in self.filters.prefetch_related('subfilters').all():
                if item.type == 'CheckBox':
                    price_to = price_to + item.subfilters.aggregate(Sum("price", default=0))["price__sum"]
                else:
                    price_to = price_to + item.subfilters.aggregate(Max("price", default=0))["price__max"]
            if self.runs:
                price_to = self.price_per_run * 10 + price_to
            return price_to
        return None

    def price_from(self):
        price_from = self.price
        if self.filters.count():
            for item in self.filters.prefetch_related('subfilters').all():
                if item.type != 'CheckBox':
                    price_from = price_from + item.subfilters.aggregate(Min("price", default=0))["price__min"]
            if self.runs:
                price_from = self.price_per_run + price_from
            return price_from
        return None

    def sale_price_to(self):
        if self.sale_active():
            sale = (self.price_to() * self.sale_percent) / 100
            return self.price_to() - sale
        return None

    def sale_price_from(self):
        if self.sale_active():
            sale = (self.price_from() * self.sale_percent) / 100
            return self.price_from() - sale
        return None

    def sale_price(self):
        if self.sale_active():
            sale = (self.price * self.sale_percent) / 100
            return self.price - sale
        return None

    def sale_active(self):
        current_datetime = timezone.now()
        if self.sale_until and self.sale_from and self.sale_until > current_datetime > self.sale_from:
            return True
        return False

    def sale_period(self):
        if self.sale_active():
            difference = self.sale_until - timezone.now()
            difference = difference - timedelta(microseconds=difference.microseconds)
            return str(difference) if difference < timedelta(hours=24) else None
        return None

    class Meta:
        ordering = ['-bought_count']
        verbose_name = 'Products'
        verbose_name_plural = 'Products'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tags'
        verbose_name_plural = 'Tags'


class Filter(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('Select', 'Select'), ('Radio', 'Radio'), ('CheckBox', 'CheckBox')])
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='filters')

    class Meta:
        verbose_name = 'Filters'
        verbose_name_plural = 'Filters'


class SubFilter(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    filter = models.ForeignKey("Filter", on_delete=models.CASCADE, related_name='subfilters', null=True)
