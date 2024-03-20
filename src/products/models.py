# -*- coding: utf-8 -*-
"""
    In this module described models for application products.

    Their purpose is storing data for products and related to products
    Models:
       Product
       Tag
       Filter
       SubFilter
"""
from datetime import timedelta
from django.db import models
from django.db.models import Max, Min, Sum
from django.utils import timezone

from src.games.models import CatalogPage
from src.products.managers.product_manager import ProductManager
from src.products.utils import get_timestamp_path


class Product(models.Model):
    """
    Description model Product.

    Additional info about the model, its purpose and use.
    Mysterious fields:
    :param image (ImageField): image for banner of product's
           page in our site.
    :param card_img (ImageField): image for card of product
           (for carousels).
    :param tab (ForeignKey): on product's page we can have tabs with
           content so this field related to Model which
           implements this logic.
    :param tag (ForeignKey): products can have specific
           status(new,limited,hot) which sites admin want to emphasize
    :param catalog_page (ForeignKey): products in system
           are related to specific catalog's page
            Catalog model implement logic of catalog's on site
    """

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_timestamp_path, null=True)
    image_alt = models.CharField(max_length=255, null=True)
    card_img = models.ImageField(upload_to=get_timestamp_path, null=True)
    card_img_alt = models.CharField(max_length=255, null=True)
    description = models.TextField()
    price = models.FloatField()
    PRICE_TYPE_CHOICES = [("fixed", "Fixed"), ("range", "Range")]
    price_type = models.CharField(max_length=10,
                                  choices=PRICE_TYPE_CHOICES)
    bonus_points = models.IntegerField(default=0)
    sale_percent = models.PositiveSmallIntegerField(blank=True, null=True)
    sale_from = models.DateTimeField(blank=True, null=True)
    sale_until = models.DateTimeField(blank=True, null=True)
    bought_count = models.IntegerField(default=0)
    catalog_page = models.ForeignKey(CatalogPage,
                                     on_delete=models.CASCADE,
                                     related_name="products",
                                     null=True)
    tag = models.ForeignKey("Tag",
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def price_to(self) -> float | None:
        """
        Method calculate max price for product with price type range.

        Calculating includes all filters and fundamental price
        """
        price_to = self.price
        if self.filters.count():
            for item in self.filters.prefetch_related("subfilters").all():
                if item.type == "CheckBox":
                    price_to = (price_to +
                                item.subfilters.aggregate(
                                    Sum("price", default=0)
                                )["price__sum"]
                                )
                else:
                    price_to = (price_to +
                                item.subfilters.aggregate(
                                    Max("price", default=0)
                                )["price__max"]
                                )
            return price_to
        return None

    def price_from(self) -> float | None:
        """
        Method calculate min price for product with price type range.

        Calculating includes all filters and fundamental price
        """
        price_from = self.price
        if self.filters.count():
            for item in self.filters.prefetch_related("subfilters").all():
                if item.type != "CheckBox":
                    price_from = (price_from +
                                  item.subfilters.aggregate(
                                      Min("price", default=0)
                                  )["price__min"]
                                  )
            return price_from
        return None

    def sale_price_to(self) -> float | None:
        """
        Method calculates max price for product with price type range.

        Calculating includes all filters, fundamental price
        and ability of sale if sale exists
        """
        if self.sale_active():
            sale = (self.price_to() * self.sale_percent) / 100
            return self.price_to() - sale
        return None

    def sale_price_from(self) -> float | None:
        """
        Method calculates min price for product with price type range.

        Calculating includes all filters, fundamental price and ability
        of sale if sale exists
        """
        if self.sale_active():
            sale = (self.price_from() * self.sale_percent) / 100
            return self.price_from() - sale
        return None

    def sale_price(self) -> float | None:
        """
        Method calculates min price for product with price fixed range.

        Calculating includes  ability of sale if sale exists
        """
        if self.sale_active():
            sale = (self.price * self.sale_percent) / 100
            return self.price - sale
        return None

    def sale_active(self) -> bool:
        """
        Method checks if sale exist in the time range
        of two fields, sale_from and sale_until
        """
        current_datetime = timezone.now()
        if (self.sale_until and self.sale_from and
                self.sale_until > current_datetime > self.sale_from):
            return True
        return False

    def sale_period(self) -> str | None:
        """
        Method shows timer(hour:minute:second)
        in str format if period of sale less than 24 hours
        """
        if self.sale_active():
            difference = self.sale_until - timezone.now()
            difference = (difference -
                          timedelta(microseconds=difference.microseconds))
            return str(difference) \
                if difference < timedelta(hours=24) else None
        return None

    class Meta:
        ordering = ["-bought_count"]
        verbose_name = "Products"
        verbose_name_plural = "Products"
        db_table = 'products'


class Tag(models.Model):
    """
    Model for storing specific statuses for products in site.

    which admin want to emphasize
    """

    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tags"
        verbose_name_plural = "Tags"
        db_table = 'tags'


class Filter(models.Model):
    """
    Model for storing filters for products in site.

    this entity helps to specify extra attributes for product
    to pay additional price
    """

    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=[("Select", "Select"),
                 ("Radio", "Radio"),
                 ("CheckBox", "CheckBox"),
                 ("Slider", "Slider")],
    )
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name="filters")
    order = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.product.title}  ({self.title})"

    class Meta:
        ordering = ['order', ]
        verbose_name = "Filters"
        verbose_name_plural = "Filters"
        db_table = 'filters'


class SubFilter(models.Model):
    """
    Model for storing filter inputs.

    with specific title and price
    """

    title = models.CharField(max_length=255)
    price = models.FloatField()
    filter = models.ForeignKey("Filter",
                               on_delete=models.CASCADE,
                               related_name="subfilters",
                               null=True)
    order = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ['order', ]
        verbose_name = "SubFilter"
        verbose_name_plural = "SubFilters"
        db_table = 'sub_filters'


class ProductTabs(models.Model):
    """
    Model for storing specific statuses for products in site.

    which admin want to emphasize
    """

    title = models.CharField()
    content = models.TextField()
    order = models.PositiveIntegerField(null=True)
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE,
                                null=True, related_name='tabs')

    class Meta:
        ordering = ['order', ]
        verbose_name = "Product Tab"
        verbose_name_plural = "Product Tabs"
        db_table = 'product_tabs'
