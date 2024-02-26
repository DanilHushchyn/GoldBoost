from django.db import models

from src.games.models import Game
from src.website.utils import get_timestamp_path


# Create your models here.

class WhyChooseUs(models.Model):
    class Meta:
        verbose_name = 'WhyChooseUs'
        verbose_name_plural = 'WhyChooseUs'


class WhyChooseUsItem(models.Model):
    icon = models.ImageField(upload_to=get_timestamp_path, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('WhyChooseUs', on_delete=models.CASCADE, related_name='items', null=True)

    class Meta:
        verbose_name = 'WhyChooseUs Item'
        verbose_name_plural = 'WhyChooseUs Items'


class Insta(models.Model):
    class Meta:
        verbose_name = 'Insta'
        verbose_name_plural = 'Insta'


class InstaImg(models.Model):
    img = models.ImageField(upload_to=get_timestamp_path, null=True)
    parent = models.ForeignKey('Insta', on_delete=models.CASCADE, related_name='imgs', null=True)

    class Meta:
        verbose_name = 'Insta Imgs'
        verbose_name_plural = 'Insta Imgs'


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
    stars_count = models.PositiveSmallIntegerField()
    source_of_review = models.CharField(max_length=255)
    date_published = models.DateField()

    class Meta:
        verbose_name = 'Reviews'
        verbose_name_plural = 'Reviews'
