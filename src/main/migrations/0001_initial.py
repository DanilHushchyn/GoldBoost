# -*- coding: utf-8 -*-
# Generated by Django 5.0.2 on 2024-03-06 11:35

import django.db.models.deletion
from django.db import migrations, models

import src.products.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("games", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Insta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("img", models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
            ],
            options={
                "verbose_name": "Insta",
                "verbose_name_plural": "Insta",
            },
        ),
        migrations.CreateModel(
            name="PromoCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=215)),
                ("from_date", models.DateField(help_text="Example: 12/12/2023")),
                ("until_date", models.DateField(help_text="Example: 12/12/2023")),
                ("discount", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Promo codes",
                "verbose_name_plural": "Promo codes",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("author", models.CharField(max_length=255, null=True)),
                ("comment", models.TextField()),
                ("stars_count", models.FloatField()),
                ("source_of_review", models.CharField(max_length=255)),
                ("date_published", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
                "ordering": ["-date_published"],
            },
        ),
        migrations.CreateModel(
            name="Setting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("instagram_nickname", models.CharField(max_length=255)),
                ("instagram_link", models.URLField()),
                ("facebook_link", models.URLField()),
                ("reddit_link", models.URLField()),
                ("email", models.EmailField(max_length=254)),
                ("discord_link", models.URLField()),
                ("whats_up_link", models.URLField()),
                ("header_top_text", models.CharField(max_length=255)),
                ("footer_bottom_text", models.CharField(max_length=255)),
                ("footer_description", models.TextField()),
                ("privacy_policy_link", models.URLField()),
                ("terms_of_use_link", models.URLField()),
                ("refund_policy_link", models.URLField()),
                ("address1", models.CharField(max_length=255)),
                ("address2", models.CharField(max_length=255)),
                ("subscribe_form_text", models.CharField(max_length=255)),
                ("subscribe_sale", models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                "verbose_name": "Settings",
                "verbose_name_plural": "Settings",
            },
        ),
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name="WhyChooseUs",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("icon", models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ("icon_alt", models.CharField(max_length=255, null=True)),
                ("title", models.CharField(max_length=25, null=True)),
                ("description", models.TextField(null=True)),
            ],
            options={
                "verbose_name": "WhyChooseUs",
                "verbose_name_plural": "WhyChooseUs",
            },
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="", max_length=255)),
                ("image", models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ("image_alt", models.CharField(max_length=255, null=True)),
                ("description", models.TextField()),
                ("date_published", models.DateField(auto_now_add=True)),
                ("game", models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="games.game")),
            ],
            options={
                "verbose_name": "News",
                "verbose_name_plural": "News",
                "ordering": ["-date_published"],
            },
        ),
    ]
