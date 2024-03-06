# -*- coding: utf-8 -*-
"""Django Admin Configuration

This module defines the admin site configuration
for the Django project. It registers Django models
with the admin site to allow for easy management and viewing of data
through the Django admin interface.

Usage:
    To register a model with the admin site, use the
    `@admin.register()` decorator:

    ```
    @admin.register(ModelName)
    class ModelNameAdminClass(ModelAdmin):
        pass
    ```

For more information on the Django admin site, see the Django documentation:
https://docs.djangoproject.com/en/stable/ref/contrib/admin/
"""

from django import forms
from django.contrib import admin
from django.contrib.admin import TabularInline
from unfold.widgets import (
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldBooleanWidget,
)

from src.products.models import Filter, Product, SubFilter, Tag


class ProductForm(forms.ModelForm):
    """ModelForm configuration for the model Product.
    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("bought_count",)
        widgets = {
            "title": UnfoldAdminTextInputWidget(attrs={}),
            "subtitle": UnfoldAdminTextInputWidget(attrs={}),
            "price_per_run": UnfoldAdminDecimalFieldWidget(attrs={}),
            "sale_percent": UnfoldAdminIntegerFieldWidget(attrs={}),
            "sale_until": UnfoldAdminSplitDateTimeWidget(attrs={}),
            "sale_from": UnfoldAdminSplitDateTimeWidget(attrs={}),
            "bonus_points": UnfoldAdminIntegerFieldWidget(attrs={}),
            "price": UnfoldAdminDecimalFieldWidget(attrs={}),
            "description": UnfoldAdminTextareaWidget(attrs={}),
            "tab": UnfoldAdminSelect(attrs={}),
            "filter": UnfoldAdminSelect(attrs={}),
            "catalog_page": UnfoldAdminSelect(attrs={}),
            "tag": UnfoldAdminSelect(attrs={}),
            "price_type": UnfoldAdminSelect(attrs={}),
            "runs": UnfoldBooleanWidget(attrs={}),
            "sale": UnfoldBooleanWidget(attrs={}),
        }


class TagForm(forms.ModelForm):
    """
    ModelForm configuration for the model Tag.
    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {
            "name": UnfoldAdminTextInputWidget(attrs={}),
            "color": UnfoldAdminTextInputWidget(attrs={}),
        }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for model Tag.
    This class defines the behavior of the Tag admin interface,
    including the displayed fields, list filters, search fields, and action.
    For more information on Django admin customization,
    see the Django documentation:
    https://docs.djangoproject.com/en/stable/ref/contrib/admin/
    """

    form = TagForm


class FilterForm(forms.ModelForm):
    """
    ModelForm configuration for the model Filter.
    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = Filter
        fields = "__all__"
        widgets = {
            "title": UnfoldAdminTextInputWidget(attrs={}),
            "type": UnfoldAdminSelect(attrs={}),
            "product": UnfoldAdminSelect(attrs={}),
        }


class SubFilterForm(forms.ModelForm):
    """
    ModelForm configuration for the model SubFilter.
    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = SubFilter
        fields = "__all__"
        widgets = {
            "title": UnfoldAdminTextInputWidget(attrs={}),
            "price": UnfoldAdminDecimalFieldWidget(attrs={}),
        }


class SubFilterInline(TabularInline):
    """
    TabularInline configuration for the model SubFilter.
    This class defines behaviour for setting multiple
    model instance on one page in django admin
    """

    model = SubFilter
    extra = 1
    form = SubFilterForm


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    """
    Admin configuration for model Filter.
    This class defines the behavior of the Filter admin interface,
    including the displayed fields, list filters, search fields, and action.
    For more information on Django admin customization,
    see the Django documentation:
    https://docs.djangoproject.com/en/stable/ref/contrib/admin/
    """

    form = FilterForm
    inlines = [
        SubFilterInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for model Product.
    This class defines the behavior of the Product admin interface,
    including the displayed fields, list filters, search fields, and action.
    For more information on Django admin customization,
    see the Django documentation:
    https://docs.djangoproject.com/en/stable/ref/contrib/admin/
    """

    form = ProductForm
