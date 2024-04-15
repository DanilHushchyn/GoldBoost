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

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import TabularInline
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.widgets import (
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget, UnfoldAdminSplitDateTimeWidget,
)

from src.products.models import Filter, FreqBought, Product, ProductTabs, SubFilter, Tag

IS_POPUP_VAR = "_popup"


class ProductForm(forms.ModelForm):
    """ModelForm configuration for the model Product.

    This class defines the appearance for form in
    admin panel django
    """

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

    def clean_type(self):
        type = self.cleaned_data["type"]
        if type == "Slider":
            msg = (
                f"If you want type Slider. \n"
                f"Firstly remove all current "
                f"sub filters and left old filter type, "
                f"than return to set type Slider and new subfilters."
            )
            for sub in self.instance.subfilters.all():
                if (len(sub.title_en) > 2 or
                        len(sub.title_en) > 2 or
                        sub.price > 9999):
                    raise forms.ValidationError(msg)
        return type


class SubFilterForm(forms.ModelForm):
    """
    ModelForm configuration for the model SubFilter.

    This class defines the appearance for form in
    admin panel django
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title_en"].required = True
        self.fields["title_uk"].required = True
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["title_en"].widget.attrs["readonly"] = True
            self.fields["title_uk"].widget.attrs["readonly"] = True

    def clean_title_en(self):
        title_en = self.cleaned_data["title_en"]
        if len(title_en) > 2 and self.instance.filter.type == "Slider":
            msg = "Max length is 2"
            raise forms.ValidationError(msg)
        return title_en

    def clean_title_uk(self):
        title_uk = self.cleaned_data["title_uk"]
        if len(title_uk) > 2 and self.instance.filter.type == "Slider":
            msg = "Max length is 2"
            raise forms.ValidationError(msg)
        return title_uk

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price > 9999 and self.instance.filter.type == "Slider":
            msg = "Max value is 9999"
            raise forms.ValidationError(msg)
        return price

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
    extra = 1
    max_num = 10
    form = SubFilterForm


@admin.register(Filter)
class FilterAdmin(ModelAdmin):
    """
    Admin configuration for model Filter.

    """

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
    list_display = ["title", "price_type", "catalog_page", ]
    list_filter = ("price_type", "catalog_page", "tag",
                   "sale_from",
                   "sale_until",)
    search_fields = ["title"]

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for product in queryset:
            [item.delete() for item in product.cart_items.all()]
            product.is_deleted = True
            product.save()

    def delete_model(self, request, obj: Product):
        [item.delete() for item in obj.cart_items.all()]
        obj.is_deleted = True
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["products"].queryset = Product.objects.filter(price_type="fixed")

    class Meta:
        model = FreqBought
        fields = "__all__"


@admin.register(FreqBought)
class FreqBoughtAdmin(ModelAdmin):
    """
    Admin configuration for model FreqBought.

    """

    form = FreqBoughtForm
