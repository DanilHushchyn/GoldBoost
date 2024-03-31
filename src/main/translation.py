from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(WhyChooseUs)
class WhyChooseUsTranslationOptions(TranslationOptions):
    fields = ('icon_alt', 'title', 'description')
    required_languages = ('en', 'ua')


@register(Insta)
class InstaTranslationOptions(TranslationOptions):
    fields = ('img_alt',)
    required_languages = ('en', 'ua')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'image_alt', 'description')
    required_languages = ('en', 'ua')


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('author', 'comment')
    required_languages = ('en', 'ua')


@register(Setting)
class SettingTranslationOptions(TranslationOptions):
    fields = ('header_top_text', 'footer_description',
              'address1', 'address2', 'subscribe_form_text')
    required_languages = ('en', 'ua')


@register(OrderItemAttribute)
class OrderItemAttributeTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('en', 'ua')
