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
from django.contrib.admin import AdminSite
from imagekit.admin import AdminThumbnail
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter, RangeDateFilter
from unfold.widgets import (
    UnfoldAdminEmailInputWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSingleDateWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminImageFieldWidget,
)

from src.main.models import Insta, News, PromoCode, Review, Setting, WhyChooseUs
import defusedxml.cElementTree as et
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import ImageField


def validate_image_file_extension(value):
    return validators.FileExtensionValidator(
        allowed_extensions=validators.get_available_image_extensions() + ['svg']
    )(value)


class ImageAndSvgField(ImageField):
    default_validators = [validate_image_file_extension]

    def to_python(self, data):
        try:
            f = super().to_python(data)
        except ValidationError as e:
            if e.code != 'invalid_image':
                raise

            # Give it a chance - maybe its SVG!
            f = data
            if not self.is_svg(f):
                # Nope it is not.
                raise

            f.content_type = 'image/svg+xml'
            if hasattr(f, "seek") and callable(f.seek):
                f.seek(0)
        return f

    def is_svg(self, f):
        if hasattr(f, "seek") and callable(f.seek):
            f.seek(0)

        try:
            doc = et.parse(f)
            root = doc.getroot()
            return root.tag == '{http://www.w3.org/2000/svg}svg'
        except et.ParseError:
            return False


# Register your models here.


class NewsForm(forms.ModelForm):
    """
    ModelForm configuration for the model News.

    This class defines the appearance for form in
    admin panel django
    """
    description_en = forms.CharField(max_length=500,
                                     min_length=100,
                                     help_text='max: 500, min: 100',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))
    description_uk = forms.CharField(max_length=500,
                                     min_length=100,
                                     help_text='max: 500, min: 100',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))
    title_en = forms.CharField(max_length=65,
                               min_length=1,
                               help_text='max: 65, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=65,
                               min_length=1,
                               help_text='max: 65, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    image_alt_en = forms.CharField(max_length=65,
                                   min_length=1,
                                   help_text='max: 65, min: 1',
                                   widget=UnfoldAdminTextInputWidget(attrs={}))
    image_alt_uk = forms.CharField(max_length=65,
                                   min_length=1,
                                   help_text='max: 65, min: 1',
                                   widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = News
        fields = "__all__"
        exclude = ["title", "image_alt", "description"]
        field_classes = {
            'image': ImageAndSvgField,
        }


@admin.register(News)
class NewsAdminClass(ModelAdmin):
    """
    Admin configuration for model News.

    This class defines the behavior of the News admin interface,
    For more information on Django admin customization,
    """
    list_display = ["title", "game", "date_published"]
    list_filter = ["game", "date_published", ]
    search_fields = ["title"]
    form = NewsForm


class ReviewForm(forms.ModelForm):
    """
    ModelForm configuration for the model Review.

    This class defines the appearance for form in
    admin panel django
    """

    author_en = forms.CharField(max_length=100,
                                min_length=1,
                                help_text='max: 100, min: 1',
                                widget=UnfoldAdminTextInputWidget(attrs={}))
    author_uk = forms.CharField(max_length=100,
                                min_length=1,
                                help_text='max: 100, min: 1',
                                widget=UnfoldAdminTextInputWidget(attrs={}))
    comment_en = forms.CharField(max_length=500,
                                 min_length=100,
                                 help_text='max: 500, min: 100',
                                 widget=UnfoldAdminTextareaWidget(attrs={}))
    comment_uk = forms.CharField(max_length=500,
                                 min_length=100,
                                 help_text='max: 500, min: 100',
                                 widget=UnfoldAdminTextareaWidget(attrs={}))
    source_of_review = forms.CharField(max_length=65,
                                       min_length=1,
                                       help_text='max: 65, min: 1',
                                       widget=UnfoldAdminTextareaWidget(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author_en"].required = True
        self.fields["author_uk"].required = True

        self.fields["comment_en"].required = True
        self.fields["comment_uk"].required = True

    class Meta:
        model = Review
        fields = "__all__"
        exclude = ["author", "comment"]


@admin.register(Review)
class ReviewAdminClass(ModelAdmin):
    """
    Admin configuration for model Review.

    This class defines the behavior of the Review admin interface,
    For more information on Django admin customization,
    """
    list_display = ["author", 'stars_count', "comment",
                    'source_of_review', "date_published"]
    list_filter = ["stars_count", "source_of_review", "author", ]
    search_fields = ["author", 'comment']
    form = ReviewForm


class WhyChooseUsForm(forms.ModelForm):
    """
    ModelForm configuration for the model WhyChooseUs.

    This class defines the appearance for form in
    admin panel django
    """
    title_en = forms.CharField(max_length=13,
                               min_length=1,
                               help_text='max: 13, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=13,
                               min_length=1,
                               help_text='max: 13, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    icon_alt_en = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextInputWidget(attrs={}))
    icon_alt_uk = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextInputWidget(attrs={}))
    description_en = forms.CharField(max_length=160,
                                     min_length=10,
                                     help_text='max: 160, min: 10',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))
    description_uk = forms.CharField(max_length=160,
                                     min_length=10,
                                     help_text='max: 160, min: 10',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))

    # icon = ImageAndSvgField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title_en"].required = True
        self.fields["title_uk"].required = True
        self.fields["icon_alt_en"].required = True
        self.fields["icon_alt_uk"].required = True
        self.fields["description_en"].required = True
        self.fields["description_uk"].required = True

    class Meta:
        model = WhyChooseUs
        fields = "__all__"
        exclude = ("title", "icon_alt", "description")
        field_classes = {
            'icon': ImageAndSvgField,
        }
        widgets = {
            'icon': UnfoldAdminImageFieldWidget(attrs={'accept': '.svg,.png,.jpeg,.jpg,.webp'})
        }


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
        if WhyChooseUs.objects.count() < 3:
            # If an instance already exists,
            # prevent creation of another instance
            return False
        else:
            # Allow creation of the first instance
            return True

    def has_add_permission(self, request):
        # Check if any instance already exists
        if WhyChooseUs.objects.count() >= 3:
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
    img_alt_en = forms.CharField(max_length=100,
                                 min_length=1,
                                 help_text='max: 100, min: 1',
                                 widget=UnfoldAdminTextInputWidget(attrs={}))
    img_alt_uk = forms.CharField(max_length=100,
                                 min_length=1,
                                 help_text='max: 100, min: 1',
                                 widget=UnfoldAdminTextInputWidget(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["img_alt_en"].required = True
        self.fields["img_alt_uk"].required = True

    class Meta:
        model = Insta
        fields = "__all__"
        exclude = [
            "img_alt",
        ]
        field_classes = {
            'img': ImageAndSvgField,
        }


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
        if Insta.objects.count() < 6:
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
    instagram_nickname = forms.CharField(max_length=30,
                                         min_length=1,
                                         help_text='max: 30, min: 1',
                                         widget=UnfoldAdminTextInputWidget(attrs={}))
    header_top_text_en = forms.CharField(max_length=100,
                                         min_length=1,
                                         help_text='max: 100, min: 1',
                                         widget=UnfoldAdminTextInputWidget(attrs={}))
    header_top_text_uk = forms.CharField(max_length=100,
                                         min_length=1,
                                         help_text='max: 100, min: 1',
                                         widget=UnfoldAdminTextInputWidget(attrs={}))
    footer_bottom_text = forms.CharField(max_length=100,
                                         min_length=1,
                                         help_text='max: 100, min: 1',
                                         widget=UnfoldAdminTextInputWidget(attrs={}))
    footer_description_en = forms.CharField(max_length=500,
                                            min_length=1,
                                            help_text='max: 500, min: 1',
                                            widget=UnfoldAdminTextareaWidget(attrs={}))
    footer_description_uk = forms.CharField(max_length=500,
                                            min_length=1,
                                            help_text='max: 500, min: 1',
                                            widget=UnfoldAdminTextareaWidget(attrs={}))
    address1_en = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextareaWidget(attrs={}))
    address1_uk = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextareaWidget(attrs={}))
    address2_en = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextareaWidget(attrs={}))
    address2_uk = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextareaWidget(attrs={}))
    subscribe_form_text_en = forms.CharField(max_length=100,
                                             min_length=1,
                                             help_text='max: 100, min: 1',
                                             widget=UnfoldAdminTextInputWidget(attrs={}))
    subscribe_form_text_uk = forms.CharField(max_length=100,
                                             min_length=1,
                                             help_text='max: 100, min: 1',
                                             widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = Setting
        fields = "__all__"
        exclude = ["header_top_text", "address1",
                   "address2", "subscribe_form_text",
                   "footer_description"]


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
    code = forms.CharField(max_length=100,
                           min_length=1,
                           help_text='max: 100, min: 1',
                           widget=UnfoldAdminTextInputWidget(attrs={}))

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
    list_display = ["code", 'from_date', "until_date",
                    'discount']
    list_filter = ["from_date", "until_date", "discount", ]
    search_fields = ["code", 'comment']

    def has_change_permission(self, request, obj=None):
        return False

    form = PromoCodeForm
