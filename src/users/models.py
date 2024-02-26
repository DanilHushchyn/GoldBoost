from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None,
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'


class Character(models.Model):
    FACTION_CHOICES = (
        ('Alliance', 'Alliance'),
        ('Horde', 'Horde'),
    )

    CLASS_SPEC_CHOICES = (
        ('Warrior - Arms', 'Warrior - Arms'),
        ('Warrior - Fury', 'Warrior - Fury'),
        ('Warrior - Protection', 'Warrior - Protection'),
        ('Paladin - Holy', 'Paladin - Holy'),
        ('Paladin - Protection', 'Paladin - Protection'),
        ('Paladin - Retribution', 'Paladin - Retribution'),
        ('Hunter - Beast Mastery', 'Hunter - Beast Mastery'),
        ('Hunter - Marksmanship', 'Hunter - Marksmanship'),
        ('Hunter - Survival', 'Hunter - Survival'),
        ('Rogue - Assassination', 'Rogue - Assassination'),
        ('Rogue - Outlaw', 'Rogue - Outlaw'),
        ('Rogue - Subtlety', 'Rogue - Subtlety'),
        ('Priest - Discipline', 'Priest - Discipline'),
        ('Priest - Holy', 'Priest - Holy'),
        ('Priest - Shadow', 'Priest - Shadow'),
        ('Death Knight - Blood', 'Death Knight - Blood'),
        ('Death Knight - Frost', 'Death Knight - Frost'),
        ('Death Knight - Unholy', 'Death Knight - Unholy'),
        ('Shaman - Elemental', 'Shaman - Elemental'),
        ('Shaman - Enhancement', 'Shaman - Enhancement'),
        ('Shaman - Restoration', 'Shaman - Restoration'),
        ('Mage - Arcane', 'Mage - Arcane'),
        ('Mage - Fire', 'Mage - Fire'),
        ('Mage - Frost', 'Mage - Frost'),
        ('Warlock - Affliction', 'Warlock - Affliction'),
        ('Warlock - Demonology', 'Warlock - Demonology'),
        ('Warlock - Destruction', 'Warlock - Destruction'),
        ('Monk - Brewmaster', 'Monk - Brewmaster'),
        ('Monk - Mistweaver', 'Monk - Mistweaver'),
        ('Monk - Windwalker', 'Monk - Windwalker'),
        ('Druid - Balance', 'Druid - Balance'),
        ('Druid - Feral', 'Druid - Feral'),
        ('Druid - Guardian', 'Druid - Guardian'),
        ('Druid - Restoration', 'Druid - Restoration'),
        ('Demon Hunter - Havoc', 'Demon Hunter - Havoc'),
        ('Demon Hunter - Vengeance', 'Demon Hunter - Vengeance'),
    )

    battle_tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    faction = models.CharField(max_length=10, choices=FACTION_CHOICES)
    additional_info = models.TextField()
    class_and_spec = models.CharField(max_length=255, choices=CLASS_SPEC_CHOICES)
    realm = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)  # Assuming User model exists
