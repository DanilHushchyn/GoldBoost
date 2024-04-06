# -*- coding: utf-8 -*-
"""
    In this module described models for application users
    Their purpose is storing data for users
    and access control system in our site
    Models:
       User
       PasswordResetToken
"""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """
    Custom user manager it's manager for making request to User model
    here is redefined some methods for saving
    user and superuser with email instead of username
    """

    def _create_user(self, email: str, password: str, **extra_fields) \
            -> object:
        """
        Create and save a user with the given username, email, and password.
        :rtype: User
        :param email: email for new user
        :param password: password for new user
        :param extra_fields: others extra
        :return: User model instance
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields) -> object:
        """
        Create and save a user with the given username, email, and password.
        :rtype: User
        :param email: email for new user
        :param password: password for new user
        :param extra_fields: others extra fields
        :return: User model instance
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,
                         email: str = None,
                         password: str = None,
                         **extra_fields)\
            -> object:
        """
        Create and save a superuser with the given email,
        password and extra fields.
        :rtype: User
        :param email: email for new user
        :param password: password for new user
        :param extra_fields: others extra fields
        :return: User model instance
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    This is our Auth Model in the site
    It's stores all data about users and provides
    some methods for creating users
    """
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)

    # username = (None,)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, unique=True)
    notify_me = models.BooleanField(default=False)
    bonus_points = models.PositiveIntegerField(default=0)

    PAYMENT_METHOD = (
        ("PayPal", "PayPal"),
        ("Visa", "Visa"),
        ("MasterCard", "MasterCard"),
        ("AmericanExpress", "AmericanExpress"),
    )
    COMMUNICATION_METHOD = (
        ("Telegram", "Telegram"),
        ("Viber", "Viber"),
        ("Discord", "Discord"),
        ("Skype", "Skype"),
        ("Facebook", "Facebook"),
        ("WhatsApp", "WhatsApp"),
    )
    payment_method = models.CharField(max_length=255,
                                      choices=PAYMENT_METHOD,
                                      default='PayPal')
    communication = models.CharField(max_length=255,
                                     choices=COMMUNICATION_METHOD,
                                     default='Discord')
    subscribe_sale_active = models.BooleanField(null=True,blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"
        db_table = 'users'


class Character(models.Model):
    """
    Model for storing characters,
    this entity exist in user's cabinet and
    has purely symbolic meaning
    """

    FACTION_CHOICES = (
        ("Alliance", "Alliance"),
        ("Horde", "Horde"),
    )

    CLASS_SPEC_CHOICES = (
        ("Warrior", "Warrior"),
        ("Paladin", "Paladin"),
        ("Hunter", "Hunter"),
        ("Rogue", "Rogue"),
        ("Priest", "Priest"),
        ("Shaman", "Shaman"),
        ("Mage", "Mage"),
        ("Warlock", "Warlock"),
        ("Monk", "Monk"),
        ("Druid", "Druid"),
    )

    battle_tag = models.CharField(max_length=255, default='battle_tag')
    name = models.CharField(max_length=255, default='name')
    faction = models.CharField(max_length=10,
                               choices=FACTION_CHOICES,
                               default='Alliance')
    additional_info = models.TextField(default='')
    class_and_spec = models.CharField(max_length=255,
                                      choices=CLASS_SPEC_CHOICES,
                                      default='Warrior')
    realm = models.CharField(max_length=255, default='')
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    date_published = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "characters"
        ordering = ['-date_published']


class PasswordResetToken(models.Model):
    """
    Model for storing tokens created for users who want to reset
    their passwords
    """

    user = models.ForeignKey("User", null=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "password_reset_token"


class Subscriber(models.Model):
    """
    Model is storing data
    about users who want to get news
    from the site
    """

    email = models.EmailField(unique=True)

    class Meta:
        db_table = "subscribers"
