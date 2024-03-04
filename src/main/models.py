from django.db import models

from src.games.models import Game
from src.users.models import User
from src.website.utils import get_timestamp_path


# Create your models here.


class WhyChooseUs(models.Model):
    icon = models.ImageField(upload_to=get_timestamp_path, null=True)
    icon_alt = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=25, null=True)
    description = models.TextField(null=True)

    class Meta:
        verbose_name = 'WhyChooseUs'
        verbose_name_plural = 'WhyChooseUs'


class Insta(models.Model):
    img = models.ImageField(upload_to=get_timestamp_path, null=True)

    class Meta:
        verbose_name = 'Insta'
        verbose_name_plural = 'Insta'


class News(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to=get_timestamp_path, null=True)
    image_alt = models.CharField(max_length=255,null=True)
    description = models.TextField()
    date_published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-date_published']


class Review(models.Model):
    author = models.CharField(max_length=255, null=True)
    comment = models.TextField()
    stars_count = models.FloatField()
    source_of_review = models.CharField(max_length=255)
    date_published = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_published']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


# Create your models here.
class Setting(models.Model):
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
    address2 = models.CharField(max_length=255)
    subscribe_form_text = models.CharField(max_length=255)
    subscribe_sale = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return "Configure settings"

    def save(self, *args, **kwargs):
        if Setting.objects.exists() and not self.pk:
            # If an instance already exists, prevent creation of another instance
            raise ValueError("Settings instance already exists")
        return super(Setting, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'


class Subscriber(models.Model):
    email = models.EmailField()


class PromoCode(models.Model):
    code = models.CharField(max_length=215)
    from_date = models.DateField(help_text='Example: 12/12/2023')
    until_date = models.DateField(help_text='Example: 12/12/2023')
    discount = models.IntegerField(default=0)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Promo codes'
        verbose_name_plural = 'Promo codes'
