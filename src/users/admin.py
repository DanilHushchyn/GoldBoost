# -*- coding: utf-8 -*-
"""Django Admin Configuration

This module defines the admin site configuration for
the Django project. It registers Django models with
 the admin site to allow for easy management and viewing of data
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
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp,EmailAddress
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, AdminPasswordChangeForm
from ninja_jwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from ninja_jwt.models import TokenUser
from django import forms
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSplitDateTimeWidget, UnfoldAdminSelect

from src.users.models import User


class UserForm(forms.ModelForm):
    """
    ModelForm configuration for the model Communication.
    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        widgets = {
            "email": UnfoldAdminTextInputWidget(attrs={}),
            "first_name": UnfoldAdminTextInputWidget(attrs={}),
            "last_name": UnfoldAdminTextInputWidget(attrs={}),
            "password": UnfoldAdminTextInputWidget(attrs={}),
            "password1": UnfoldAdminTextInputWidget(attrs={}),
            "password2": UnfoldAdminTextInputWidget(attrs={}),
            "payment_method": UnfoldAdminTextInputWidget(attrs={}),
            "communication": UnfoldAdminTextInputWidget(attrs={}),
            "last_login": UnfoldAdminSplitDateTimeWidget(attrs={}),
            "date_joined": UnfoldAdminSplitDateTimeWidget(attrs={}),
        }


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Admin configuration for model User.
    This class defines the behavior of the User admin interface,
    including the displayed fields, list filters, search fields, and action.
    For more information on Django admin customization,
    see the Django documentation:
    https://docs.djangoproject.com/en/stable/ref/contrib/admin/
    """

    model = User
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", 'payment_method', 'communication')}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]

    form = UserForm

    def has_add_permission(self, request):
        return False


admin.site.unregister(SocialAccount)


# admin.site.register(User, CustomUserAdmin)
@admin.register(SocialAccount)
class CustomSocialAccountAdmin(ModelAdmin):
    pass


admin.site.unregister(SocialToken)


# admin.site.register(User, CustomUserAdmin)
@admin.register(SocialToken)
class CustomSocialAccountAdmin(ModelAdmin):
    pass


admin.site.unregister(SocialApp)


# admin.site.register(User, CustomUserAdmin)
@admin.register(SocialApp)
class CustomSocialAccountAdmin(ModelAdmin):
    pass


admin.site.unregister(BlacklistedToken)


# admin.site.register(User, CustomUserAdmin)
@admin.register(BlacklistedToken)
class CustomBlackAdmin(ModelAdmin):
    pass


admin.site.unregister(OutstandingToken)


# admin.site.register(User, CustomUserAdmin)
@admin.register(OutstandingToken)
class CustomBlackAdmin(ModelAdmin):
    pass


admin.site.unregister(EmailAddress)
admin.site.unregister(Group)

