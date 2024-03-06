# -*- coding: utf-8 -*-
"""Django Admin Configuration

This module defines the admin site configuration for the Django project. It registers
Django models with the admin site to allow for easy management and viewing of data
through the Django admin interface.

Usage:
    To register a model with the admin site, use the `@admin.register()` decorator:

    ```
    @admin.register(Game)
    class GameAdminClass(ModelAdmin):
        pass
    ```

For more information on the Django admin site, see the Django documentation:
https://docs.djangoproject.com/en/stable/ref/contrib/admin/
"""
from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.widgets import (
    UnfoldAdminImageFieldWidget,
    UnfoldAdminSingleDateWidget,
    UnfoldAdminSingleTimeWidget,
    UnfoldAdminTextareaWidget,
)

from src.games.models import Calendar, CalendarItem, CatalogPage, Game, Tab, TabItem, WorthLookCarouselItem


# Register your models here.
class TabItemForm(forms.ModelForm):
    class Meta:
        model = TabItem
        fields = "__all__"
        widgets = {
            "content": UnfoldAdminTextareaWidget(attrs={"summernote": "true"}),
        }


class TabItemInline(TabularInline):
    model = TabItem
    form = TabItemForm


class WorthItemsInline(TabularInline):
    model = WorthLookCarouselItem


@admin.register(Tab)
class TabAdminClass(ModelAdmin):
    inlines = [
        TabItemInline,
    ]


@admin.register(Game)
class GameAdminClass(ModelAdmin):
    pass


class CalendarItemForm(forms.ModelForm):
    class Meta:
        model = CalendarItem
        fields = "__all__"
        widgets = {
            "date": UnfoldAdminSingleDateWidget(attrs={"style": "width: 200px;"}),
            "team1_img": UnfoldAdminImageFieldWidget(attrs={"style": "width: 10px;"}),
            "team2_img": UnfoldAdminImageFieldWidget(attrs={"style": "width: 10px;"}),
            "team1_from": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
            "team2_from": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
            "team1_until": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
            "team2_until": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
        }


class CalendarInline(TabularInline):
    model = CalendarItem
    form = CalendarItemForm


@admin.register(Calendar)
class CalendarAdminClass(ModelAdmin):
    inlines = [
        CalendarInline,
    ]


@admin.register(CatalogPage)
class CatalogPagesAdminClass(ModelAdmin):
    inlines = [
        WorthItemsInline,
    ]
