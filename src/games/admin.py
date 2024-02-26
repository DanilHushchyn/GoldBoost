from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.games.models import TabItem, WorthLookCarouselItem, Tab, CatalogPage


# Register your models here.
class TabItemsInline(TabularInline):
    model = TabItem


class WorthItemsInline(TabularInline):
    model = WorthLookCarouselItem


@admin.register(Tab)
class TabsAdminClass(ModelAdmin):
    inlines = [
        TabItemsInline,
    ]


@admin.register(CatalogPage)
class CatalogPagesAdminClass(ModelAdmin):
    inlines = [
        WorthItemsInline,
    ]
