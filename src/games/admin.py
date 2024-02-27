from django.contrib import admin
from django import forms
from unfold.admin import ModelAdmin, TabularInline
from unfold.widgets import UnfoldAdminSingleDateWidget, UnfoldAdminImageFieldWidget, UnfoldAdminSingleTimeWidget, \
    UnfoldAdminTextareaWidget

from src.games.models import TabItem, WorthLookCarouselItem, Tab, CatalogPage, CalendarItem, Calendar, Game


# Register your models here.
class TabItemForm(forms.ModelForm):
    class Meta:
        model = TabItem
        fields = '__all__'
        widgets = {
            'content': UnfoldAdminTextareaWidget(attrs={'summernote': "true"}),
        }
class TabItemInline(TabularInline):
    model = TabItem
    form = TabItemForm

class WorthItemsInline(TabularInline):
    model = WorthLookCarouselItem


@admin.register(Tab)
class TabAdminClass(ModelAdmin):
    inlines = [
        TabItemInline,
    ]


@admin.register(Game)
class GameAdminClass(ModelAdmin):
    pass


class CalendarItemForm(forms.ModelForm):
    class Meta:
        model = CalendarItem
        fields = '__all__'
        widgets = {
            'date': UnfoldAdminSingleDateWidget(attrs={'style': 'width: 200px;'}),
            'team1_img': UnfoldAdminImageFieldWidget(attrs={'style': 'width: 10px;'}),
            'team2_img': UnfoldAdminImageFieldWidget(attrs={'style': 'width: 10px;'}),
            'team1_from': UnfoldAdminSingleTimeWidget(attrs={'style': 'width: 200px;'}),
            'team2_from': UnfoldAdminSingleTimeWidget(attrs={'style': 'width: 200px;'}),
            'team1_until': UnfoldAdminSingleTimeWidget(attrs={'style': 'width: 200px;'}),
            'team2_until': UnfoldAdminSingleTimeWidget(attrs={'style': 'width: 200px;'}),
        }


class CalendarInline(TabularInline):
    model = CalendarItem
    form = CalendarItemForm


@admin.register(Calendar)
class CalendarAdminClass(ModelAdmin):
    inlines = [
        CalendarInline,
    ]





@admin.register(CatalogPage)
class CatalogPagesAdminClass(ModelAdmin):
    inlines = [
        WorthItemsInline,
    ]
