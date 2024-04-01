# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions, register

from .models import *


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("title", "subtitle", "image_alt", "card_img_alt", "description")
    required_languages = ("en", "uk")


@register(Filter)
class FilterTranslationOptions(TranslationOptions):
    fields = ("title",)
    required_languages = ("en", "uk")


@register(SubFilter)
class SubFilterTranslationOptions(TranslationOptions):
    fields = ("title",)
    required_languages = ("en", "uk")


@register(ProductTabs)
class ProductTabsTranslationOptions(TranslationOptions):
    fields = ("title", "content")
    required_languages = ("en", "uk")


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("name",)
    required_languages = ("en", "uk")
