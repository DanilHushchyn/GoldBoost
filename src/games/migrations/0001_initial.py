# -*- coding: utf-8 -*-
# Generated by Django 5.0.2 on 2024-03-04 17:36

import django.db.models.deletion
import meta.models
from django.db import migrations, models

import src.products.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Calendar",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Calendars",
                "verbose_name_plural": "Calendars",
            },
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("logo_filter", models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ("logo_product", models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ("logo_filter_alt", models.CharField(max_length=255, null=True)),
                ("logo_product_alt", models.CharField(max_length=255, null=True)),
                ("order", models.IntegerField(null=True)),
            ],
            options={
                "verbose_name": "Games",
                "verbose_name_plural": "Games",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Tab",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
            options={
                "verbose_name": "Tab",
                "verbose_name_plural": "Tabs",
            },
        ),
        migrations.CreateModel(
            name="CalendarItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("team1_img", models.ImageField(upload_to="")),
                ("team1_img_alt", models.CharField(max_length=255, null=True)),
                ("team1_from", models.TimeField()),
                ("team1_until", models.TimeField()),
                ("team2_img", models.ImageField(upload_to="")),
                ("team2_img_alt", models.CharField(max_length=255, null=True)),
                ("team2_from", models.TimeField()),
                ("team2_until", models.TimeField()),
                (
                    "calendar",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="games.calendar"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CatalogPage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField()),
                ("description", models.TextField()),
                (
                    "calendar",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="games.calendar"
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="games.catalogpage",
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="catalog_pages",
                        related_query_name="game",
                        to="games.game",
                    ),
                ),
                (
                    "tab",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_query_name="tab_content",
                        to="games.tab",
                    ),
                ),
            ],
            options={
                "verbose_name": "Catalog Page",
                "verbose_name_plural": "Catalog Pages",
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name="TabItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField()),
                ("content", models.TextField()),
                ("order", models.PositiveIntegerField(null=True)),
                (
                    "tab",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, related_name="tab_items", to="games.tab"
                    ),
                ),
            ],
            options={
                "verbose_name": "Tab Item",
                "verbose_name_plural": "Tab Items",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="WorthLookCarouselItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ("image_alt", models.CharField(max_length=255, null=True)),
                ("title", models.CharField()),
                ("link", models.URLField()),
                (
                    "catalog_page",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="worth_items",
                        to="games.catalogpage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Worth look carousel",
                "verbose_name_plural": "Worth look carousel",
            },
        ),
    ]
