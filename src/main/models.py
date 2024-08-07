# -*- coding: utf-8 -*-
"""
    In this module described models for application main.

    Their purpose is storing data for common entities in our site
    Models:
       WhyChooseUs
       Insta
       News
       Review
       Setting
       PromoCode
       Subscriber
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill

from src.games.models import Game
from src.main.tasks import share_news
from src.orders.models import Order
from src.products.models import FreqBought, Product, SubFilter
from src.products.utils import get_timestamp_path, make_sale
from src.users.models import User

# Create your models here.


class WhyChooseUs(models.Model):
    """
    Model is storing content for section WhyChooseUs on the main page.

    """

    icon = models.ImageField(upload_to=get_timestamp_path, null=True)
    icon_alt = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "WhyChooseUs"
        verbose_name_plural = "WhyChooseUs"
        db_table = "why_choose_us"


class Insta(models.Model):
    """
    Model is storing content for section Instagram on the main page.

    """

    img = models.ImageField(upload_to=get_timestamp_path, null=True)
    img_thumbnail = ImageSpecField(
        source="img", processors=[ResizeToFill(180, 183)], format="PNG", options={"quality": 90}
    )
    img_alt = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.img_alt

    class Meta:
        verbose_name = "Insta"
        verbose_name_plural = "Insta"
        db_table = "insta"


class News(models.Model):
    """
    Model is storing content for section News on the main page.

    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, default="")
    image = models.ImageField(upload_to=get_timestamp_path, null=True)
    image_alt = models.CharField(max_length=255, null=True)
    description = models.TextField()
    date_published = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        String format for News models instance.

        :return: str
        """
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            share_news.delay(news_title=self.title, news_descr=self.description)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-date_published"]
        db_table = "news"


class Review(models.Model):
    """
    Model is storing content for section Review on the main page.

    """

    author = models.CharField(max_length=255, null=True)
    comment = models.TextField()
    stars_count = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    source_of_review = models.CharField(max_length=255)
    source_of_review_url = models.URLField(null=True)
    date_published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.author

    class Meta:
        ordering = ["-date_published"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        db_table = "reviews"


# Create your models here.
class Setting(models.Model):
    """
    Model is storing content for header and footer in the site.

    """

    instagram_nickname = models.CharField(max_length=255)
    instagram_link = models.URLField()
    facebook_link = models.URLField()
    reddit_link = models.URLField()
    email = models.EmailField()
    discord_link = models.URLField()
    whats_up_link = models.URLField()
    header_top_text = models.CharField(max_length=255)
    footer_bottom_text = models.CharField(max_length=255)
    footer_description = models.TextField()
    privacy_policy_link = models.URLField()
    terms_of_use_link = models.URLField()
    refund_policy_link = models.URLField()
    address1 = models.CharField(max_length=255)
    address1_link = models.URLField(null=True)
    address2 = models.CharField(max_length=255)
    address2_link = models.URLField(null=True)
    subscribe_form_text = models.CharField(max_length=255)
    subscribe_sale = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        """
        String format for Setting models instance.

        :return: str
        """
        return "Configure settings"

    def save(self, *args, **kwargs):
        """
        Purpose of this method to make constraint.

        (not more than 1 Setting model instance in the site)
        """
        if Setting.objects.exists() and not self.pk:
            # If an instance already exists, prevent creation of another instance
            raise ValueError("Settings instance already exists")
        return super(Setting, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
        db_table = "settings"


class PromoCode(models.Model):
    """
    Model is storing data about all promo codes in the site.

    """

    code = models.CharField(max_length=215)
    from_date = models.DateField()
    until_date = models.DateField()
    discount = models.IntegerField(default=0)
    users = models.ManyToManyField(User, related_name="promo_codes")

    def __str__(self):
        """
        String format for Setting models instance.

        :return: code of promo code
        """
        return self.code

    class Meta:
        verbose_name = "Promo codes"
        verbose_name_plural = "Promo codes"
        db_table = "promo_codes"


class OrderItem(models.Model):
    """
    Model represents order's items.

    """

    cost = models.FloatField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    )
    freqbot = models.ForeignKey(
        FreqBought,
        on_delete=models.SET_NULL,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def price_for_product(self, product: Product):
        total = product.price
        for attr in self.attributes.all():
            total = total + attr.subfilter.price
        if product.sale_active():
            if product.price_type == "fixed":
                total = product.sale_price()
            else:
                total = make_sale(total, product.sale_percent)
        return total * self.quantity

    def price(self):
        if self.product:
            return self.price_for_product(self.product)
        else:
            total = 0
            for product in self.freqbot.products.all():
                total = total + self.price_for_product(product)
            return make_sale(total, self.freqbot.discount)

    def bonus_points(self):
        if self.product:
            return self.product.bonus_points * self.quantity
        else:
            total = 0
            for product in self.freqbot.products.all():
                total = total + product.bonus_points
            return total

    class Meta:
        ordering = ["-date_created"]
        db_table = "sub_orders"


class OrderItemAttribute(models.Model):
    """
    Model represents order's item attributes.

    """

    title = models.CharField(max_length=255, null=True)
    subtitle = models.CharField(max_length=255, null=True)
    subfilter = models.ForeignKey(
        SubFilter,
        on_delete=models.SET_NULL,
        null=True,
    )
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="attributes",
        null=True,
    )

    class Meta:
        db_table = "sub_orders_attributes"
