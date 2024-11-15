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
import json

from celery.utils.dispatch.signal import Signal
from django import forms
from django.contrib import admin, messages
from django.contrib.admin import TabularInline
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from loguru import logger
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.widgets import (
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminImageFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
)

from src.main.admin import ImageAndSvgField
from src.products.models import Filter, FreqBought, Product, ProductTabs, SubFilter, Tag

IS_POPUP_VAR = "_popup"


class ProductForm(forms.ModelForm):
    """ModelForm configuration for the model Product.

    This class defines the appearance for form in
    admin panel django
    """
    description_en = forms.CharField(max_length=1000,
                                     min_length=100,
                                     help_text='max: 1000, min: 100',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))
    description_uk = forms.CharField(max_length=1000,
                                     min_length=100,
                                     help_text='max: 1000, min: 100',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))
    title_en = forms.CharField(max_length=70,
                               min_length=1,
                               help_text='max: 70, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=70,
                               min_length=1,
                               help_text='max: 70, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    subtitle_en = forms.CharField(max_length=70,
                                  min_length=1,
                                  help_text='max: 70, min: 1',
                                  widget=UnfoldAdminTextInputWidget(attrs={}))
    subtitle_uk = forms.CharField(max_length=70,
                                  min_length=1,
                                  help_text='max: 70, min: 1',
                                  widget=UnfoldAdminTextInputWidget(attrs={}))
    card_img_alt_en = forms.CharField(max_length=70,
                                      min_length=1,
                                      help_text='max: 70, min: 1',
                                      widget=UnfoldAdminTextInputWidget(attrs={}))
    card_img_alt_uk = forms.CharField(max_length=70,
                                      min_length=1,
                                      help_text='max: 70, min: 1',
                                      widget=UnfoldAdminTextInputWidget(attrs={}))
    image_alt_en = forms.CharField(max_length=70,
                                   min_length=1,
                                   help_text='max: 70, min: 1',
                                   widget=UnfoldAdminTextInputWidget(attrs={}))
    image_alt_uk = forms.CharField(max_length=70,
                                   min_length=1,
                                   help_text='max: 70, min: 1',
                                   widget=UnfoldAdminTextInputWidget(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and not instance.pk:
            self.fields["sale_percent"].widget = UnfoldAdminTextInputWidget(attrs={"value": 0})

        if instance and instance.pk:
            self.fields["price_type"].widget = forms.HiddenInput()
            self.fields["catalog_page"].widget = forms.HiddenInput()

    class Meta:
        model = Product
        exclude = [
            "title",
            "subtitle",
            "image_alt",
            "card_img_alt",
            "description",
            "bought_count",
            "is_deleted",
        ]
        field_classes = {
            'card_img': ImageAndSvgField,
            'image': ImageAndSvgField,
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0.25:
            msg = "Min value is 0.25"
            raise forms.ValidationError(msg)
        return price

    def clean_sale_percent(self):
        sale_percent = self.cleaned_data["sale_percent"]
        if sale_percent is None or sale_percent < 0:
            msg = "Min value is 0"
            raise forms.ValidationError(msg)
        return sale_percent

    def clean_bonus_points(self):
        bonus_points = self.cleaned_data["bonus_points"]
        if bonus_points < 1:
            msg = "Min value is 1"
            raise forms.ValidationError(msg)
        return bonus_points


class TagForm(forms.ModelForm):
    """
    ModelForm configuration for the model Tag.

    This class defines the appearance for form in
    admin panel django
    """
    name_en = forms.CharField(max_length=20,
                              min_length=1,
                              help_text='max: 20, min: 1',
                              widget=UnfoldAdminTextInputWidget(attrs={}))
    name_uk = forms.CharField(max_length=20,
                              min_length=1,
                              help_text='max: 20, min: 1',
                              widget=UnfoldAdminTextInputWidget(attrs={}))
    color = forms.CharField(max_length=70,
                            min_length=1,
                            help_text='max: 70, min: 1',
                            widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = Tag
        fields = "__all__"
        exclude = [
            "name",
        ]
        widgets = {
            "name_en": UnfoldAdminTextInputWidget(attrs={}),
            "name_uk": UnfoldAdminTextInputWidget(attrs={}),
            "color": UnfoldAdminTextInputWidget(attrs={}),
        }


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    """
    Admin configuration for model Tag.

    """

    form = TagForm

    def delete_model(self, request, obj: Tag):
        # Customize the logic here before deleting the object
        # For instance, you can perform additional actions or checks
        # such as preventing deletion of specific instances
        if obj.id == 1:
            msg = "Unable to delete tag HOT (very important tag)."
            messages.add_message(request, messages.ERROR, msg)

            return False
            # request.user.message_set.create(message='Message text here')
        # Perform any other necessary actions
        obj.delete()  # Delete the object

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        if 1 in queryset.values_list("id", flat=True):
            msg = "Unable to delete tag HOT (very important tag)."
            messages.add_message(request, messages.ERROR, msg)
            return False
        queryset.delete()

    def response_delete(self, request, obj_display, obj_id):
        """
        Determine the HttpResponse for the delete_view stage.
        """
        if IS_POPUP_VAR in request.POST:
            popup_response_data = json.dumps(
                {
                    "action": "delete",
                    "value": str(obj_id),
                }
            )
            return TemplateResponse(
                request,
                self.popup_response_template
                or [
                    "admin/%s/%s/popup_response.html" % (self.opts.app_label, self.opts.model_name),
                    "admin/%s/popup_response.html" % self.opts.app_label,
                    "admin/popup_response.html",
                ],
                {
                    "popup_response_data": popup_response_data,
                },
            )
        if obj_id == 1:
            pass
        else:
            self.message_user(
                request,
                "The %(name)s “%(obj)s” was deleted successfully."
                % {
                    "name": self.opts.verbose_name,
                    "obj": obj_display,
                },
                messages.SUCCESS,
            )

        if self.has_change_permission(request, None):
            post_url = reverse(
                "admin:%s_%s_changelist" % (self.opts.app_label, self.opts.model_name),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({"preserved_filters": preserved_filters, "opts": self.opts}, post_url)
        else:
            post_url = reverse("admin:index", current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)


class FilterForm(forms.ModelForm):
    """
    ModelForm configuration for the model Filter.

    This class defines the appearance for form in
    admin panel django
    """
    title_en = forms.CharField(max_length=70,
                               min_length=1,
                               help_text='max: 70, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=70,
                               min_length=1,
                               help_text='max: 70, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        self.fields["title_en"].required = True
        self.fields["title_uk"].required = True
        products = Product.objects.filter(price_type="range")
        self.fields["product"].queryset = products
        self.fields["product"].required = True
        if instance and instance.pk:
            self.fields["product"].widget = forms.HiddenInput()
            self.fields["type"].widget = UnfoldAdminTextInputWidget(attrs={})
            self.fields["type"].widget.attrs["readonly"] = True

            # self.fields["type"].widget.attrs["isDisabled"] = True

    class Meta:
        model = Filter
        fields = "__all__"
        exclude = ["title"]
        widgets = {
            "title_en": UnfoldAdminTextInputWidget(attrs={}),
            "title_uk": UnfoldAdminTextInputWidget(attrs={}),
            "type": UnfoldAdminSelect(attrs={}),
            "product": UnfoldAdminSelect(attrs={}),
            "order": UnfoldAdminTextInputWidget(attrs={}),
        }

    # def clean_type(self):
    #     type = self.cleaned_data["type"]
    #     if type == "Slider":
    #         msg = (
    #             f"If you want type Slider. \n"
    #             f"Firstly remove all current "
    #             f"sub filters and left old filter type, "
    #             f"than return to set type Slider and new subfilters."
    #         )
    #         for sub in self.instance.subfilters.all():
    #             if len(sub.title_en) > 2 or len(sub.title_en) > 2 or sub.price > 9999:
    #                 raise forms.ValidationError(msg)
    #     return type


class SubFilterForm(forms.ModelForm):
    """
    ModelForm configuration for the model SubFilter.

    This class defines the appearance for form in
    admin panel django
    """
    title_en = forms.CharField(max_length=30,
                               min_length=1,
                               help_text='max: 30, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=30,
                               min_length=1,
                               help_text='max: 30, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title_en"].required = True
        self.fields["title_uk"].required = True
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["title_en"].widget.attrs["readonly"] = True
            self.fields["title_uk"].widget.attrs["readonly"] = True



    class Meta:
        model = SubFilter
        fields = "__all__"
        exclude = ["title"]

        widgets = {
            "title_en": UnfoldAdminTextInputWidget(attrs={}),
            "title_uk": UnfoldAdminTextInputWidget(attrs={}),
            "price": UnfoldAdminDecimalFieldWidget(attrs={}),
            "order": UnfoldAdminTextInputWidget(attrs={}),
        }


class SubFilterInline(TabularInline):
    """
    TabularInline configuration for the model SubFilter.

    This class defines behaviour for setting multiple
    model instance on one page in django admin
    """

    model = SubFilter
    extra = 0
    max_num = 10
    min_num = 1
    form = SubFilterForm

    def has_delete_permission(self, request, obj: Filter = None):
        if obj and obj.subfilters.count() <= 1:
            return False
        return True


@admin.register(Filter)
class FilterAdmin(ModelAdmin):
    """
    Admin configuration for model Filter.

    """

    list_display = ["title", "type", "product"]
    list_filter = [
        "type",
        "product",
    ]
    search_fields = ["title"]

    form = FilterForm
    inlines = [
        SubFilterInline,
    ]


class ProductTabsForm(forms.ModelForm):
    """
    ModelForm configuration for the model ProductTabs.

    This class defines the appearance for form in
    admin panel django
    """
    title_en = forms.CharField(max_length=20,
                               min_length=1,
                               help_text='max: 20, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=20,
                               min_length=1,
                               help_text='max: 20, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    content_en = forms.CharField(max_length=2000,
                                 min_length=100,
                                 help_text='max: 2000, min: 100',
                                 widget=UnfoldAdminTextareaWidget(attrs={"summernote": "true"}))
    content_uk = forms.CharField(max_length=2000,
                                 min_length=100,
                                 help_text='max: 2000, min: 100',
                                 widget=UnfoldAdminTextareaWidget(attrs={"summernote": "true"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title_en"].required = True
        self.fields["title_uk"].required = True
        self.fields["content_en"].required = False
        self.fields["content_uk"].required = False

    class Meta:
        model = ProductTabs
        fields = "__all__"
        exclude = ["title", "content"]

        widgets = {
            "title_en": UnfoldAdminTextInputWidget(attrs={"style": "width: 200px;"}),
            "title_uk": UnfoldAdminTextInputWidget(attrs={"style": "width: 200px;"}),
            "content_en": UnfoldAdminTextareaWidget(attrs={"summernote": "true"}),
            "content_uk": UnfoldAdminTextareaWidget(attrs={"summernote": "true"}),
            "order": UnfoldAdminIntegerFieldWidget(attrs={"style": "width: 80px"}),
        }


class ProductTabsInline(TabularInline):
    """
    TabularInline configuration for the model ProductTabs.

    This class defines behaviour for setting multiple
    model instance on one page in django admin
    """

    model = ProductTabs
    extra = 1
    form = ProductTabsForm


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Admin configuration for model Product.

    """

    list_display = [
        "title",
        "catalog_page",
    ]
    list_filter = (
        "price_type",
        "catalog_page",
        "tag",
        "sale_from",
        "sale_until",
    )
    search_fields = ["title"]

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for product in queryset:
            [item.delete() for item in product.cart_items.all()]
            product.is_deleted = True
            [tab.delete() for tab in product.tabs.all()]
            freqbots = product.freqbought_set.all()
            FreqBoughtAdmin.delete_queryset(self, request, freqbots)
            product.save()

    def delete_model(self, request, obj: Product):
        [item.delete() for item in obj.cart_items.all()]
        obj.is_deleted = True
        [tab.delete() for tab in obj.tabs.all()]
        freqbots = obj.freqbought_set.all()
        FreqBoughtAdmin.delete_queryset(self, request, freqbots)
        obj.save()
        return True

    inlines = [
        ProductTabsInline,
    ]
    form = ProductForm


class FreqBoughtForm(forms.ModelForm):
    """
    ModelForm configuration for the model FreqBought.

    This class defines the appearance for form in
    admin panel django
    """
    title = forms.CharField(max_length=100,
                            min_length=1,
                            help_text='max: 100, min: 1',
                            widget=UnfoldAdminTextInputWidget(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        self.fields["products"].queryset = Product.objects.filter(price_type="fixed")
        if instance and instance.pk:
            self.fields["products"].disabled = True

    def clean_products(self):
        products = self.cleaned_data["products"]
        if len(products) < 2:
            msg = "You have to choose minimum 2 products"
            raise forms.ValidationError(msg)
        if len(products) > 6:
            msg = "You can choose maximum 6 products"
            raise forms.ValidationError(msg)
        return products

    def clean_discount(self):
        discount = self.cleaned_data["discount"]
        if discount < 1:
            msg = "Min value is 1"
            raise forms.ValidationError(msg)
        return discount

    class Meta:
        model = FreqBought
        fields = [
            "title",
            "order",
            "products",
            "discount",
        ]
        widgets = {
            "products": FilteredSelectMultiple(verbose_name="Products with fixed price",
                                               is_stacked=True)
        }


@admin.register(FreqBought)
class FreqBoughtAdmin(ModelAdmin):
    """
    Admin configuration for model FreqBought.

    """

    list_display = [
        "title",
        "discount",
    ]
    search_fields = ["title"]
    form = FreqBoughtForm

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for freqbot in queryset:
            [item.delete() for item in freqbot.cart_items.all()]
            freqbot.is_deleted = True
            freqbot.save()

    def delete_model(self, request, obj: FreqBought):
        [item.delete() for item in obj.cart_items.all()]
        obj.is_deleted = True
        obj.save()
        return True

    def has_add_permission(self, request, obj: FreqBought = None):
        if FreqBought.objects.count() < 4:
            return True
        return False
