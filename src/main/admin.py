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

For more information on the Django admin site,
see the Django documentation:
https://docs.djangoproject.com/en/stable/ref/contrib/admin/
"""

from django import forms
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from unfold.admin import ModelAdmin
from unfold.widgets import (
    UnfoldAdminEmailInputWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSingleDateWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
)

from src.main.models import Insta, News, PromoCode, Review, Setting, WhyChooseUs


# Register your models here.

class NewsForm(forms.ModelForm):
    """
    ModelForm configuration for the model News.

    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = News
        fields = "__all__"
        exclude = ['title', 'image_alt', 'description']


@admin.register(News)
class NewsAdminClass(ModelAdmin):
    """
    Admin configuration for model News.

    This class defines the behavior of the News admin interface,
    For more information on Django admin customization,
    """

    form = NewsForm


class ReviewForm(forms.ModelForm):
    """
    ModelForm configuration for the model Review.

    This class defines the appearance for form in
    admin panel django
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_en'].required = True
        self.fields['author_uk'].required = True

        self.fields['comment_en'].required = True
        self.fields['comment_uk'].required = True

    class Meta:
        model = Review
        fields = "__all__"
        exclude = ['author', 'comment']


@admin.register(Review)
class ReviewAdminClass(ModelAdmin):
    """
    Admin configuration for model Review.

    This class defines the behavior of the Review admin interface,
    For more information on Django admin customization,
    """

    form = ReviewForm


class WhyChooseUsForm(forms.ModelForm):
    """
    ModelForm configuration for the model WhyChooseUs.

    This class defines the appearance for form in
    admin panel django
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_en'].required = True
        self.fields['title_uk'].required = True
        self.fields['icon_alt_en'].required = True
        self.fields['icon_alt_uk'].required = True
        self.fields['description_en'].required = True
        self.fields['description_uk'].required = True

    class Meta:
        model = WhyChooseUs
        fields = "__all__"
        exclude = ("title", "icon_alt", "description")


@admin.register(WhyChooseUs)
class WhyChooseUsAdminClass(ModelAdmin):
    """
    Admin configuration for model WhyChooseUs.

    This class defines the behavior of the WhyChooseUs admin interface,
    For more information on Django admin customization,
    """
    form = WhyChooseUsForm

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


class InstaForm(forms.ModelForm):
    """
    ModelForm configuration for the model Insta.

    This class defines the appearance for form in
    admin panel django
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img_alt_en'].required = True
        self.fields['img_alt_uk'].required = True

    class Meta:
        model = Insta
        fields = "__all__"
        exclude = ['img_alt', ]


@admin.register(Insta)
class InstaAdminClass(ModelAdmin):
    """
    Admin configuration for model Insta.

    This class defines the behavior of the Insta admin interface,
    For more information on Django admin customization,
    """
    form = InstaForm

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
        exclude = ['header_top_text',
                   'address1', 'address2',
                   'subscribe_form_text',
                   'footer_description']


@admin.register(Setting)
class SettingAdmin(ModelAdmin):
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
class PromoCodeAdmin(ModelAdmin):
    """
    Admin configuration for model PromoCode.

    This class defines the behavior of the PromoCode admin interface,
    For more information on Django admin customization,
    """
    def has_change_permission(self, request, obj=None):
        return False
    form = PromoCodeForm
