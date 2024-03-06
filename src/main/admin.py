# -*- coding: utf-8 -*-
"""Django Admin Configuration

This module defines the admin site configuration for the Django project. It registers
Django models with the admin site to allow for easy management and viewing of data
through the Django admin interface.

Usage:
    To register a model with the admin site, use the `@admin.register()` decorator:

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
from unfold.admin import ModelAdmin, TabularInline
from unfold.widgets import (
    UnfoldAdminDateWidget,
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldBooleanWidget,
)

from src.main.models import Insta, News, PromoCode, Review, Setting, Subscriber, WhyChooseUs

# Register your models here.


@admin.register(News)
class NewsAdminClass(ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdminClass(ModelAdmin):
    pass


@admin.register(WhyChooseUs)
class WhyChooseUsAdminClass(ModelAdmin):
    pass


@admin.register(Insta)
class InstaAdminClass(ModelAdmin):
    pass


# Register your models here.
class SettingsForm(forms.ModelForm):
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
    form = SettingsForm

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission for all instances
        return False

    def has_add_permission(self, request):
        # Check if any instance already exists
        if Setting.objects.exists():
            # If an instance already exists, prevent creation of another instance
            return False
        else:
            # Allow creation of the first instance
            return True


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = "__all__"
        exclude = ("users",)
        widgets = {
            "code": UnfoldAdminTextInputWidget(attrs={}),
            "from_date": UnfoldAdminDateWidget(attrs={}),
            "until_date": UnfoldAdminDateWidget(attrs={}),
            "discount": UnfoldAdminIntegerFieldWidget(attrs={}),
        }


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    form = PromoCodeForm
