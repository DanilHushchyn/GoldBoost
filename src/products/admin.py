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
from unfold.admin import ModelAdmin
from django.contrib import admin

from django.contrib.admin import TabularInline
from unfold.widgets import (
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
)

from src.products.models import Filter, Product, SubFilter, Tag, ProductTabs, FreqBought
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import json
from django.template.response import TemplateResponse
from django.contrib.admin.templatetags.admin_urls import (
    add_preserved_filters)

IS_POPUP_VAR = "_popup"


class ProductForm(forms.ModelForm):
    """ModelForm configuration for the model Product.

    This class defines the appearance for form in
    admin panel django
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['price_type'].widget = forms.HiddenInput()
            self.fields['catalog_page'].widget = forms.HiddenInput()

    class Meta:
        model = Product
        exclude = [
            'title',
            'subtitle',
            'image_alt',
            'card_img_alt',
            'description',
            'bought_count',
            'is_deleted',
        ]
        # widgets = {
        #     "title_en": UnfoldAdminTextInputWidget(attrs={}),
        #     "title_uk": UnfoldAdminTextInputWidget(attrs={}),
        #     "subtitle_en": UnfoldAdminTextInputWidget(attrs={}),
        #     "subtitle_uk": UnfoldAdminTextInputWidget(attrs={}),
        #     "price_per_run": UnfoldAdminDecimalFieldWidget(attrs={}),
        #     "sale_percent": UnfoldAdminIntegerFieldWidget(attrs={}),
        #     "sale_until": UnfoldAdminSplitDateTimeWidget(attrs={}),
        #     "sale_from": UnfoldAdminSplitDateTimeWidget(attrs={}),
        #     "bonus_points": UnfoldAdminIntegerFieldWidget(attrs={}),
        #     "price": UnfoldAdminDecimalFieldWidget(attrs={}),
        #     "description_en": UnfoldAdminTextareaWidget(attrs={}),
        #     "description_uk": UnfoldAdminTextareaWidget(attrs={}),
        #     "tab": UnfoldAdminSelect(attrs={}),
        #     "filter": UnfoldAdminSelect(attrs={}),
        #     "catalog_page": UnfoldAdminSelect(attrs={}),
        #     "tags": SelectMultiple(attrs={"style": "width: 200px;"}),
        #     "price_type": UnfoldAdminSelect(attrs={"default": "fixed"}),
        #     "runs": UnfoldBooleanWidget(attrs={}),
        #     "sale": UnfoldBooleanWidget(attrs={}),
        #     "card_img_alt_en": UnfoldAdminTextInputWidget(attrs={}),
        #     "card_img_alt_uk": UnfoldAdminTextInputWidget(attrs={}),
        #     "image_alt_en": UnfoldAdminTextInputWidget(attrs={}),
        #     "image_alt_uk": UnfoldAdminTextInputWidget(attrs={}),
        #     "card_img": UnfoldAdminImageFieldWidget(attrs={}),
        #     "image": UnfoldAdminImageFieldWidget(attrs={}),
        #     "tag": UnfoldAdminSelect(attrs={}),
        # }


class TagForm(forms.ModelForm):
    """
    ModelForm configuration for the model Tag.

    This class defines the appearance for form in
    admin panel django
    """

    class Meta:
        model = Tag
        fields = "__all__"
        exclude = ['name', ]
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
            msg = 'Unable to delete tag HOT (very important tag).'
            messages.add_message(request,
                                 messages.ERROR,
                                 msg)

            return False
            # request.user.message_set.create(message='Message text here')
        # Perform any other necessary actions
        obj.delete()  # Delete the object

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        if 1 in queryset.values_list('id', flat=True):
            msg = 'Unable to delete tag HOT (very important tag).'
            messages.add_message(request,
                                 messages.ERROR,
                                 msg)
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
                    "admin/%s/%s/popup_response.html"
                    % (self.opts.app_label, self.opts.model_name),
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
            post_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": self.opts}, post_url
            )
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
        self.fields['title_en'].required = True
        self.fields['title_uk'].required = True

    class Meta:
        model = Filter
        fields = "__all__"
        exclude = ['title']
        widgets = {
            "title_en": UnfoldAdminTextInputWidget(attrs={}),
            "title_uk": UnfoldAdminTextInputWidget(attrs={}),
            "type": UnfoldAdminSelect(attrs={}),
            "product": UnfoldAdminSelect(attrs={}),
            "order": UnfoldAdminTextInputWidget(attrs={}),
        }


class SubFilterForm(forms.ModelForm):
    """
    ModelForm configuration for the model SubFilter.

    This class defines the appearance for form in
    admin panel django
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_en'].required = True
        self.fields['title_uk'].required = True
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['title_en'].widget.attrs['readonly'] = True
            self.fields['title_uk'].widget.attrs['readonly'] = True

    class Meta:
        model = SubFilter
        fields = "__all__"
        exclude = ['title']

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
        self.fields['title_en'].required = True
        self.fields['title_uk'].required = True
        self.fields['content_en'].required = True
        self.fields['content_uk'].required = True

    class Meta:
        model = ProductTabs
        fields = "__all__"
        exclude = ['title', 'content']

        widgets = {
            "title_en": UnfoldAdminTextInputWidget(attrs={"style": "width: 200px;"}),
            "title_uk": UnfoldAdminTextInputWidget(attrs={"style": "width: 200px;"}),
            "content_en": UnfoldAdminTextareaWidget(attrs={"summernote": "true"}),
            "content_uk": UnfoldAdminTextareaWidget(attrs={"summernote": "true"}),
            "order": UnfoldAdminIntegerFieldWidget(attrs={"style": "width: 80px;"}),
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

    # def get_form(self, request, obj=None, **kwargs):
    #     if obj is None:
    #         # Use a different form for adding new records
    #         self.form = ProductForm
    #
    #         return ProductForm
    #
    #     else:
    #         # Use a different form for updating existing records
    #         self.form = UpdateProductForm
    #         return UpdateProductForm

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
        self.fields['products'].queryset = Product.objects.filter(price_type='fixed')

    class Meta:
        model = FreqBought
        fields = "__all__"


@admin.register(FreqBought)
class FreqBoughtAdmin(ModelAdmin):
    """
    Admin configuration for model FreqBought.

    """

    form = FreqBoughtForm
