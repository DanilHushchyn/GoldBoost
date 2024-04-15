# -*- coding: utf-8 -*-
# Generated by Django 5.0.2 on 2024-04-04 18:57

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import src.users.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
            options={
                "db_table": "subscribers",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("first_name", models.CharField(max_length=255, null=True)),
                ("last_name", models.CharField(max_length=255, null=True)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("notify_me", models.BooleanField(default=False)),
                ("bonus_points", models.PositiveIntegerField(default=0)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("PayPal", "PayPal"),
                            ("Visa", "Visa"),
                            ("MasterCard", "MasterCard"),
                            ("AmericanExpress", "AmericanExpress"),
                        ],
                        default="PayPal",
                        max_length=255,
                    ),
                ),
                (
                    "communication",
                    models.CharField(
                        choices=[
                            ("Telegram", "Telegram"),
                            ("Viber", "Viber"),
                            ("Discord", "Discord"),
                            ("Skype", "Skype"),
                            ("Facebook", "Facebook"),
                            ("WhatsApp", "WhatsApp"),
                        ],
                        default="Discord",
                        max_length=255,
                    ),
                ),
                ("subscribe_sale_active", models.BooleanField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Users",
                "verbose_name_plural": "Users",
                "db_table": "users",
            },
            managers=[
                ("objects", src.users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Character",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("battle_tag", models.CharField(default="battle_tag", max_length=255)),
                ("name", models.CharField(default="name", max_length=255)),
                (
                    "faction",
                    models.CharField(
                        choices=[("Alliance", "Alliance"), ("Horde", "Horde")], default="Alliance", max_length=10
                    ),
                ),
                ("additional_info", models.TextField(default="")),
                (
                    "class_and_spec",
                    models.CharField(
                        choices=[
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
                        ],
                        default="Warrior",
                        max_length=255,
                    ),
                ),
                ("realm", models.CharField(default="", max_length=255)),
                ("date_published", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "db_table": "characters",
                "ordering": ["-date_published"],
            },
        ),
        migrations.CreateModel(
            name="PasswordResetToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.CharField(max_length=255, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "db_table": "password_reset_token",
            },
        ),
    ]
