# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions, register

from src.games.models import CalendarBlock, CalendarBlockItem, CatalogPage, CatalogTabs, Game, Team, WorthLookItem


@register(Game)
class GameTranslationOptions(TranslationOptions):
    fields = ("logo_filter_alt", "logo_product_alt")
    required_languages = ("en", "uk")


@register(CatalogPage)
class CatalogPageTranslationOptions(TranslationOptions):
    fields = ("title", "description")
    required_languages = ("en", "uk")


@register(CatalogTabs)
class CatalogTabsTranslationOptions(TranslationOptions):
    fields = ("title", "content")
    required_languages = ("en", "uk")


@register(WorthLookItem)
class WorthLookItemTranslationOptions(TranslationOptions):
    fields = ("image_alt",)
    required_languages = ("en", "uk")


@register(CalendarBlock)
class CalendarBlockTranslationOptions(TranslationOptions):
    fields = ("title", "subtitle")
    required_languages = ("en", "uk")


# @register(CalendarBlockItem)
# class CalendarBlockItemTranslationOptions(TranslationOptions):
#     fields = ('team1_img_alt', 'team2_img_alt',)
#     required_languages = ('en', 'uk')


@register(Team)
class TeamTranslationOptions(TranslationOptions):
    fields = ("team_img_alt",)
    required_languages = ("en", "uk")
