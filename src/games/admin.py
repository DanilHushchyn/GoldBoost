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
from django.core.exceptions import ValidationError
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
from src.main.admin import ImageAndSvgField
from src.products.admin import ProductAdmin


class WorthLookItemForm(forms.ModelForm):
    image_alt_en = forms.CharField(max_length=50,
                                   min_length=1,
                                   help_text='max: 50, min: 1',
                                   widget=UnfoldAdminTextInputWidget(attrs={}))
    image_alt_uk = forms.CharField(max_length=50,
                                   min_length=1,
                                   help_text='max: 50, min: 1',
                                   widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = WorthLookItem
        fields = "__all__"


class WorthLookForm(forms.ModelForm):
    title = forms.CharField(max_length=50,
                            min_length=1,
                            help_text='max: 50, min: 1',
                            widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = WorthLook
        fields = "__all__"


class WorthLookItemInline(TabularInline):
    model = WorthLookItem
    form = WorthLookItemForm
    exclude = ["image_alt"]
    extra = 0


@admin.register(WorthLook)
class WorthLookCarouselItem(ModelAdmin):
    model = WorthLook
    form = WorthLookForm
    inlines = [
        WorthLookItemInline,
    ]


class GameForm(forms.ModelForm):
    name = forms.CharField(max_length=50,
                           min_length=1,
                           help_text='max: 50, min: 1',
                           widget=UnfoldAdminTextInputWidget(attrs={}))
    logo_filter_alt_en = forms.CharField(max_length=50,
                                         min_length=1,
                                         help_text='max: 50, min: 1',
                                         widget=UnfoldAdminTextInputWidget(attrs={}))
    logo_filter_alt_uk = forms.CharField(max_length=50,
                                         min_length=1,
                                         help_text='max: 50, min: 1',
                                         widget=UnfoldAdminTextInputWidget(attrs={}))
    logo_product_alt_en = forms.CharField(max_length=50,
                                          min_length=1,
                                          help_text='max: 50, min: 1',
                                          widget=UnfoldAdminTextInputWidget(attrs={}))
    logo_product_alt_uk = forms.CharField(max_length=50,
                                          min_length=1,
                                          help_text='max: 50, min: 1',
                                          widget=UnfoldAdminTextInputWidget(attrs={}))

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

        if not self.instance.pk and Game.objects.filter(name=data).exists():
            msg = "Game with this name already exists"
            raise ValidationError(msg)

        return data

    class Meta:
        model = Game
        fields = "__all__"
        exclude = ["logo_filter_alt", "logo_product_alt", "is_deleted"]
        field_classes = {
            'logo_filter': ImageAndSvgField,
            'logo_product': ImageAndSvgField,
        }


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


class CalendarBlockForm(forms.ModelForm):
    title_en = forms.CharField(max_length=50,
                               min_length=1,
                               help_text='max: 50, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=50,
                               min_length=1,
                               help_text='max: 50, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    subtitle_en = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextInputWidget(attrs={}))
    subtitle_uk = forms.CharField(max_length=100,
                                  min_length=1,
                                  help_text='max: 100, min: 1',
                                  widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = CalendarBlock
        fields = "__all__"


@admin.register(CalendarBlock)
class CalendarBlockModelAdmin(ModelAdmin):
    model = CalendarBlock
    form = CalendarBlockForm
    list_display = [
        "title",
        "subtitle",
        "calendar",
    ]
    list_filter = [
        "calendar",
    ]
    search_fields = ["title", "subtitle"]
    exclude = ["title", "subtitle"]

    inlines = [
        CalendarBlockItemInline,
    ]


class CalendarCommonForm(forms.ModelForm):
    title = forms.CharField(max_length=100,
                            min_length=1,
                            help_text='max: 100, min: 1',
                            widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = Calendar
        fields = "__all__"


@admin.register(Calendar)
class CalendarAdminClass(ModelAdmin):
    form = CalendarCommonForm
    search_fields = ["title"]


class CatalogTabsForm(forms.ModelForm):
    """
    ModelForm configuration for the model CatalogTabs.

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
    title_en = forms.CharField(max_length=30,
                               min_length=1,
                               help_text='max: 30, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    title_uk = forms.CharField(max_length=30,
                               min_length=1,
                               help_text='max: 30, min: 1',
                               widget=UnfoldAdminTextInputWidget(attrs={}))
    description_en = forms.CharField(max_length=500,
                                     min_length=1,
                                     help_text='max: 500, min: 1',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))
    description_uk = forms.CharField(max_length=500,
                                     min_length=1,
                                     help_text='max: 500, min: 1',
                                     widget=UnfoldAdminTextareaWidget(attrs={}))

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
    list_display = ["title", "description", "game", "calendar", "worth_look"]
    list_filter = [
        "game",
    ]
    search_fields = [
        "title",
        "description",
    ]

    def delete_model(self, request, obj: CatalogPage):
        products = obj.products.all()
        ProductAdmin.delete_queryset(self, request, products)
        obj.is_deleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for page in queryset:
            products = page.products.all()
            ProductAdmin.delete_queryset(self, request, products)
            page.is_deleted = True
            page.save()


@admin.register(Game)
class GameAdminClass(ModelAdmin):
    form = GameForm
    search_fields = ["name"]

    def delete_model(self, request, obj: Game):
        pages = obj.catalog_pages.all()
        CatalogPagesAdminClass.delete_queryset(self, request, pages)
        obj.is_deleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for game in queryset:
            pages = game.catalog_pages.all()
            CatalogPagesAdminClass.delete_queryset(self, request, pages)
            game.is_deleted = True
            game.save()


class TeamForm(forms.ModelForm):
    team_img_alt_en = forms.CharField(max_length=50,
                                      min_length=1,
                                      help_text='max: 50, min: 1',
                                      widget=UnfoldAdminTextInputWidget(attrs={}))
    team_img_alt_uk = forms.CharField(max_length=50,
                                      min_length=1,
                                      help_text='max: 50, min: 1',
                                      widget=UnfoldAdminTextInputWidget(attrs={}))

    class Meta:
        model = Team
        fields = "__all__"
        field_classes = {
            'team_img': ImageAndSvgField,
        }


@admin.register(Team)
class TeamAdminClass(ModelAdmin):
    exclude = ["team_img_alt"]
    form = TeamForm
