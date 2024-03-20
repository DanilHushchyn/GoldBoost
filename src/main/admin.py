# -*- coding: utf-8 -*-
"""
Django Admin Configuration.

This module defines the admin site
configuration for the Django project. It registers
Django models with the admin site to allow for
easy management and viewing of data through the Django admin interface.

Usage:
    To register a model with the admin site,
    use the `@admin.register()` decorator:

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
from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest
from ninja.errors import HttpError
from typing_extensions import Any
from unfold.admin import ModelAdmin, TabularInline
from unfold.exceptions import UnfoldException
from unfold.widgets import (
    UnfoldAdminDateWidget,
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldBooleanWidget, UnfoldAdminSingleDateWidget,
)

from src.main.models import Insta, News, PromoCode, Review, Setting, WhyChooseUs


# Register your models here.


@admin.register(News)
class NewsAdminClass(ModelAdmin):
    """
    Admin configuration for model News.

    This class defines the behavior of the News admin interface,
    For more information on Django admin customization,
    """

    pass


@admin.register(Review)
class ReviewAdminClass(ModelAdmin):
    """
    Admin configuration for model Review.

    This class defines the behavior of the Review admin interface,
    For more information on Django admin customization,
    """

    pass


@admin.register(WhyChooseUs)
class WhyChooseUsAdminClass(ModelAdmin):
    """
    Admin configuration for model WhyChooseUs.

    This class defines the behavior of the WhyChooseUs admin interface,
    For more information on Django admin customization,
    """
    def has_delete_permission(self, request, obj=None):
        # Disable delete permission for all instances
        if WhyChooseUs.objects.count() <= 3:
            # If an instance already exists,
            # prevent creation of another instance
            return False
        else:
            # Allow creation of the first instance
            return True

    def has_add_permission(self, request):
        # Check if any instance already exists
        if WhyChooseUs.objects.count() >= 6:
            # If an instance already exists,
            # prevent creation of another instance
            return False
        else:
            # Allow creation of the first instance
            return True


@admin.register(Insta)
class InstaAdminClass(ModelAdmin):
    """
    Admin configuration for model Insta.
    This class defines the behavior of the Insta admin interface,
    For more information on Django admin customization,
    """

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission for all instances
        if Insta.objects.count() <= 6:
            # If an instance already exists,
            # prevent creation of another instance
            return False
        else:
            # Allow creation of the first instance
            return True

    def has_add_permission(self, request):
        # Check if any instance already exists
        if Insta.objects.count() >= 6:
            # If an instance already exists,
            # prevent creation of another instance
            return False
        else:
            # Allow creation of the first instance
            return True


# Register your models here.
class SettingsForm(forms.ModelForm):
    """
    ModelForm configuration for the model Setting.
    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = Setting
        fields = "__all__"
        widgets = {
            "instagram_nickname": UnfoldAdminTextInputWidget(attrs={}),
            "header_top_text": UnfoldAdminTextInputWidget(attrs={}),
            "footer_bottom_text": UnfoldAdminTextInputWidget(attrs={}),
            "address1": UnfoldAdminTextInputWidget(attrs={}),
            "address2": UnfoldAdminTextInputWidget(attrs={}),
            "subscribe_form_text": UnfoldAdminTextInputWidget(attrs={}),
            "instagram_link": UnfoldAdminTextInputWidget(attrs={}),
            "facebook_link": UnfoldAdminTextInputWidget(attrs={}),
            "reddit_link": UnfoldAdminTextInputWidget(attrs={}),
            "discord_link": UnfoldAdminTextInputWidget(attrs={}),
            "whats_up_link": UnfoldAdminTextInputWidget(attrs={}),
            "privacy_policy_link": UnfoldAdminTextInputWidget(attrs={}),
            "terms_of_use_link": UnfoldAdminTextInputWidget(attrs={}),
            "footer_description": UnfoldAdminTextareaWidget(attrs={}),
            "refund_policy_link": UnfoldAdminTextInputWidget(attrs={}),
            "subscribe_sale": UnfoldAdminIntegerFieldWidget(attrs={}),
            "email": UnfoldAdminEmailInputWidget(attrs={}),
        }


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """
    Admin configuration for model Setting.

    This class defines the behavior of the Setting admin interface,
    For more information on Django admin customization,
    """

    form = SettingsForm

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission for all instances
        return False

    def has_add_permission(self, request):
        # Check if any instance already exists
        if Setting.objects.exists():
            # If an instance already exists,
            # prevent creation of another instance
            return False
        else:
            # Allow creation of the first instance
            return True


class PromoCodeForm(forms.ModelForm):
    """
    ModelForm configuration for the model PromoCode.
    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = PromoCode
        fields = "__all__"
        exclude = ("users",)
        widgets = {
            "code": UnfoldAdminTextInputWidget(attrs={}),
            "from_date": UnfoldAdminSingleDateWidget(attrs={}),
            "until_date": UnfoldAdminSingleDateWidget(attrs={}),
            "discount": UnfoldAdminIntegerFieldWidget(attrs={}),
        }


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    """
    Admin configuration for model PromoCode.
    This class defines the behavior of the PromoCode admin interface,
    For more information on Django admin customization,
    """

    form = PromoCodeForm
