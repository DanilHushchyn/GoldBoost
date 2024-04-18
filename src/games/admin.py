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
from django.contrib import admin
from django.db.models import QuerySet
from unfold.admin import ModelAdmin, TabularInline
from unfold.widgets import (
    UnfoldAdminImageFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminSelect,
    UnfoldAdminSingleDateWidget,
    UnfoldAdminSingleTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
)

from src.games.models import (
    Calendar,
    CalendarBlock,
    CalendarBlockItem,
    CatalogPage,
    CatalogTabs,
    Game,
    Team,
    WorthLook,
    WorthLookItem,
)

from django.core.exceptions import ValidationError


class WorthLookItemInline(TabularInline):
    model = WorthLookItem
    exclude = ["image_alt"]
    extra = 0


@admin.register(WorthLook)
class WorthLookCarouselItem(ModelAdmin):
    model = WorthLook
    inlines = [
        WorthLookItemInline,
    ]


class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["logo_filter_alt_en"].required = True
        self.fields["logo_filter_alt_uk"].required = True
        self.fields["logo_product_alt_en"].required = True
        self.fields["logo_product_alt_uk"].required = True

    def clean_name(self):
        data = self.cleaned_data["name"]
        starts_with_uppercase = data[0].isupper()
        if starts_with_uppercase is not True:
            msg = "The string have to start with an uppercase letter"
            raise ValidationError(msg)

        return data

    class Meta:
        model = Game
        fields = "__all__"
        exclude = ["logo_filter_alt", "logo_product_alt", "is_deleted"]


class CalendarItemForm(forms.ModelForm):
    class Meta:
        model = CalendarBlockItem
        fields = "__all__"

        widgets = {
            "date": UnfoldAdminSingleDateWidget(attrs={"style": "width: 180px;"}),
            "team1": UnfoldAdminSelect(attrs={"style": "width: 150px;", "placeholder": "Select value"}),
            "team2": UnfoldAdminSelect(attrs={"style": "width: 150px;", "placeholder": "Select value"}),
            "team1_from": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 160px;"}),
            "team2_from": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 160px;"}),
            "team1_until": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 160px;"}),
            "team2_until": UnfoldAdminSingleTimeWidget(attrs={"style": "width: 160px;"}),
        }


class CalendarBlockItemInline(TabularInline):
    model = CalendarBlockItem
    form = CalendarItemForm
    extra = 0


@admin.register(CalendarBlock)
class CalendarBlockModelAdmin(ModelAdmin):
    model = CalendarBlock
    list_display = ["title", "subtitle",
                    'calendar', ]
    list_filter = ["calendar", ]
    search_fields = ["title", "subtitle"]
    exclude = ["title", "subtitle"]

    inlines = [
        CalendarBlockItemInline,
    ]


@admin.register(Calendar)
class CalendarAdminClass(ModelAdmin):
    search_fields = ["title"]


class CatalogTabsForm(forms.ModelForm):
    """
    ModelForm configuration for the model CatalogTabs.

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
        model = CatalogTabs
        fields = "__all__"
        exclude = ["title", "content"]

        widgets = {
            "title_en": UnfoldAdminTextInputWidget(attrs={"style": "width: 200px;"}),
            "title_uk": UnfoldAdminTextInputWidget(attrs={"style": "width: 200px;"}),
            "content_en": UnfoldAdminTextareaWidget(
                attrs={
                    "style": "width: 200px;",
                    "summernote": "true",
                }
            ),
            "content_uk": UnfoldAdminTextareaWidget(
                attrs={
                    "style": "width: 200px;",
                    "summernote": "true",
                }
            ),
            "order": UnfoldAdminIntegerFieldWidget(attrs={"style": "width: 80px;"}),
        }


class CatalogTabsInline(TabularInline):
    """
    TabularInline configuration for the model CatalogTabs.

    This class defines behaviour for setting multiple
    model instance on one page in django admin
    """

    model = CatalogTabs
    extra = 1
    form = CatalogTabsForm


class CatalogPageForm(forms.ModelForm):
    class Meta:
        model = CatalogPage
        fields = "__all__"
        exclude = ["title", "description", "is_deleted"]

    def _get_excl_ids(self, instance: CatalogPage) -> list:
        ids = []
        for item in instance.items.all():
            ids.append(item.id)
            if item.items:
                ids.extend(self._get_excl_ids(item))
        return ids

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        self.fields["parent"].widget = forms.HiddenInput()
        if instance and instance.pk:
            self.fields["game"].widget = forms.HiddenInput()
            self.fields["parent"].widget = UnfoldAdminSelect()
            pa_queryset = CatalogPage.objects.filter(game=instance.game)
            ids = self._get_excl_ids(instance)
            ids.append(instance.id)
            pa_queryset = pa_queryset.exclude(id__in=ids)
            self.fields["parent"].queryset = pa_queryset

    def save(self, commit=True):
        instance = super().save(commit=False)
        parent = instance.parent
        if parent:
            instance.game_id = parent.game.id
        return instance


@admin.register(CatalogPage)
class CatalogPagesAdminClass(ModelAdmin):
    form = CatalogPageForm
    inlines = [CatalogTabsInline]
    list_display = ["title", "description",
                    'game', "calendar", 'worth_look']
    list_filter = ["game", ]
    search_fields = ["title", "description", ]

    def delete_model(self, request, obj: CatalogPage):
        for product in obj.products.all():
            product.is_deleted = True
            [tab.delete() for tab in product.tabs.all()]
            product.save()
        obj.is_deleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for page in queryset:
            for product in page.products.all():
                product.is_deleted = True
                [tab.delete() for tab in product.tabs.all()]
                product.save()
            page.is_deleted = True
            page.save()


@admin.register(Game)
class GameAdminClass(ModelAdmin):
    form = GameForm
    search_fields = ["name"]

    def delete_model(self, request, obj: Game):
        for page in obj.catalog_pages.all():
            CatalogPagesAdminClass.delete_model(self, request, page)
        obj.is_deleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for game in queryset:
            for page in game.catalog_pages.all():
                CatalogPagesAdminClass.delete_model(self, request, page)
            game.is_deleted = True
            game.save()


@admin.register(Team)
class TeamAdminClass(ModelAdmin):
    exclude = ["team_img_alt"]
