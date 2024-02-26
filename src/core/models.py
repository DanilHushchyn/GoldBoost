from django.db import models

from src.users.models import User


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
    review_sale = models.PositiveSmallIntegerField()
    subscribe_sale = models.PositiveSmallIntegerField()

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
    from_date = models.DateField()
    until_date = models.DateField()
    discount = models.IntegerField(default=0)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Promo codes'
        verbose_name_plural = 'Promo codes'
