from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from src.main.models import News, WhyChooseUs, Review, Insta


# Register your models here.


@admin.register(News)
class NewsAdminClass(ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdminClass(ModelAdmin):
    pass


@admin.register(WhyChooseUs)
class WhyChooseUsAdminClass(ModelAdmin):
    pass


@admin.register(Insta)
class InstaAdminClass(ModelAdmin):
    pass
