# -*- coding: utf-8 -*-
"""
Django Admin Configuration.

This module defines the admin site configuration
for the Django project. It registers Django models
with the admin site to allow for easy management and viewing of data
through the Django admin interface.

Usage:
    To register a model with the admin site,
    use the `@admin.register()` decorator:

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
    UnfoldAdminTextareaWidget, UnfoldAdminTextInputWidget,
)

from src.games.models import CalendarBlock, CalendarBlockItem, CatalogPage, Game, Tab, TabItem, WorthLookItem, \
    WorthLook, Calendar


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


class WorthLookItemInline(TabularInline):
    model = WorthLookItem


@admin.register(WorthLook)
class WorthLookCarouselItem(ModelAdmin):
    model = WorthLook
    inlines = [
        WorthLookItemInline,
    ]


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
        model = CalendarBlockItem
        fields = "__all__"
        widgets = {
            "date": UnfoldAdminSingleDateWidget(attrs={"style": "width: 200px;"}),
            "team1_img": UnfoldAdminImageFieldWidget(attrs={"style": "width: 10px;"}),
            "team1_img_alt": UnfoldAdminTextInputWidget(attrs={"style": "width: 150px;"}),
            "team2_img": UnfoldAdminImageFieldWidget(attrs={"style": "width: 10px;"}),
            "team2_img_alt": UnfoldAdminTextInputWidget(attrs={"style": "width: 150px;"}),
            "team1_from": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
            "team2_from": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
            "team1_until": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
            "team2_until": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 200px;"}),
        }


class CalendarBlockItemInline(TabularInline):
    model = CalendarBlockItem
    form = CalendarItemForm


@admin.register(CalendarBlock)
class CalendarBlockModelAdmin(ModelAdmin):
    model = CalendarBlock

    inlines = [
        CalendarBlockItemInline,
    ]


@admin.register(Calendar)
class CalendarAdminClass(ModelAdmin):
    pass


@admin.register(CatalogPage)
class CatalogPagesAdminClass(ModelAdmin):
    pass
