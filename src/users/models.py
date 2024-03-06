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

    def _create_user(self, email: str, password: str, **extra_fields) -> object:
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

    def create_superuser(self, email: str = None, password: str = None, **extra_fields) -> object:
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

    username = (None,)
    email = models.EmailField(max_length=255, unique=True)
    notify_me = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"


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
        ("Warrior - Arms", "Warrior - Arms"),
        ("Warrior - Fury", "Warrior - Fury"),
        ("Warrior - Protection", "Warrior - Protection"),
        ("Paladin - Holy", "Paladin - Holy"),
        ("Paladin - Protection", "Paladin - Protection"),
        ("Paladin - Retribution", "Paladin - Retribution"),
        ("Hunter - Beast Mastery", "Hunter - Beast Mastery"),
        ("Hunter - Marksmanship", "Hunter - Marksmanship"),
        ("Hunter - Survival", "Hunter - Survival"),
        ("Rogue - Assassination", "Rogue - Assassination"),
        ("Rogue - Outlaw", "Rogue - Outlaw"),
        ("Rogue - Subtlety", "Rogue - Subtlety"),
        ("Priest - Discipline", "Priest - Discipline"),
        ("Priest - Holy", "Priest - Holy"),
        ("Priest - Shadow", "Priest - Shadow"),
        ("Death Knight - Blood", "Death Knight - Blood"),
        ("Death Knight - Frost", "Death Knight - Frost"),
        ("Death Knight - Unholy", "Death Knight - Unholy"),
        ("Shaman - Elemental", "Shaman - Elemental"),
        ("Shaman - Enhancement", "Shaman - Enhancement"),
        ("Shaman - Restoration", "Shaman - Restoration"),
        ("Mage - Arcane", "Mage - Arcane"),
        ("Mage - Fire", "Mage - Fire"),
        ("Mage - Frost", "Mage - Frost"),
        ("Warlock - Affliction", "Warlock - Affliction"),
        ("Warlock - Demonology", "Warlock - Demonology"),
        ("Warlock - Destruction", "Warlock - Destruction"),
        ("Monk - Brewmaster", "Monk - Brewmaster"),
        ("Monk - Mistweaver", "Monk - Mistweaver"),
        ("Monk - Windwalker", "Monk - Windwalker"),
        ("Druid - Balance", "Druid - Balance"),
        ("Druid - Feral", "Druid - Feral"),
        ("Druid - Guardian", "Druid - Guardian"),
        ("Druid - Restoration", "Druid - Restoration"),
        ("Demon Hunter - Havoc", "Demon Hunter - Havoc"),
        ("Demon Hunter - Vengeance", "Demon Hunter - Vengeance"),
    )

    battle_tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    faction = models.CharField(max_length=10, choices=FACTION_CHOICES)
    additional_info = models.TextField()
    class_and_spec = models.CharField(max_length=255, choices=CLASS_SPEC_CHOICES)
    realm = models.CharField(max_length=255)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)  # Assuming User model exists


class PasswordResetToken(models.Model):
    """
    Model for storing tokens created for users who want to reset
    their passwords
    """

    user = models.ForeignKey("User", null=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "password_reset_token"
