from django.db import models

from src.games.models import Game
from src.website.utils import get_timestamp_path


# Create your models here.


class WhyChooseUs(models.Model):
    icon = models.ImageField(upload_to=get_timestamp_path, null=True)
    title = models.CharField(max_length=25,null=True)
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
    description = models.TextField()
    date_published = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Review(models.Model):
    author = models.CharField(max_length=255)
    comment = models.TextField()
    stars_count = models.FloatField()
    source_of_review = models.CharField(max_length=255)
    date_published = models.DateField()

    class Meta:
        verbose_name = 'Reviews'
        verbose_name_plural = 'Reviews'
