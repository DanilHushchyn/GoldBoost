from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'image_alt',
              'card_img_alt', 'description')
    required_languages = ('en', 'ua')


@register(Filter)
class FilterTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('en', 'ua')


@register(SubFilter)
class SubFilterTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('en', 'ua')


@register(ProductTabs)
class ProductTabsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
    required_languages = ('en', 'ua')


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'ua')
