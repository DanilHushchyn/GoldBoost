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
from django.contrib import admin, messages

from django.contrib.admin import TabularInline

from unfold.admin import ModelAdmin

from unfold.widgets import (
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
)

from src.main.models import OrderItem
from src.orders.models import Order


class OrderItemInline(TabularInline):
    """
    TabularInline configuration for the model OrderItem.

    This class defines behaviour for setting multiple
    model instance on one page in django admin
    """

    model = OrderItem
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """
    Admin configuration for model Order.

    """
    list_display = ["number", "status",
                    'total_price', 'date_created']
    list_filter = ["status", "date_created", ]
    search_fields = ["number", 'total_price']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    inlines = [
        OrderItemInline,
    ]
