from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from src.main.models import News, WhyChooseUsItem, WhyChooseUs
# Register your models here.


@admin.register(News)
class NewsAdminClass(ModelAdmin):
    pass


class WhyChooseUsItemsInline(TabularInline):
    model = WhyChooseUsItem


@admin.register(WhyChooseUs)
class WhyChooseUsAdminClass(ModelAdmin):
    inlines = [
        WhyChooseUsItemsInline,
    ]

