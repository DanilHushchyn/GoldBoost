from django.contrib import admin
from django.contrib.admin import TabularInline

from src.products.models import Product, Tag, Filter, SubFilter


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class SubFilterInline(TabularInline):
    model = SubFilter


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    inlines = [
        SubFilterInline,
    ]
