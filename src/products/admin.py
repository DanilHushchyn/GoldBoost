from django.contrib import admin
from django.contrib.admin import TabularInline
from unfold.widgets import UnfoldAdminTextareaWidget, UnfoldAdminTextInputWidget, UnfoldAdminDecimalFieldWidget, \
    UnfoldAdminIntegerFieldWidget, UnfoldAdminSplitDateTimeWidget, UnfoldAdminRadioSelectWidget, UnfoldAdminSelect, \
    UnfoldBooleanWidget

from src.products.models import Product, Tag, Filter, SubFilter
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('bought_count',)
        widgets = {
            'title': UnfoldAdminTextInputWidget(attrs={}),
            'subtitle': UnfoldAdminTextInputWidget(attrs={}),
            'price_per_run': UnfoldAdminDecimalFieldWidget(attrs={}),
            'sale_percent': UnfoldAdminIntegerFieldWidget(attrs={}),
            'sale_until': UnfoldAdminSplitDateTimeWidget(attrs={}),
            'sale_from': UnfoldAdminSplitDateTimeWidget(attrs={}),
            'bonus_points': UnfoldAdminIntegerFieldWidget(attrs={}),
            'price': UnfoldAdminDecimalFieldWidget(attrs={}),
            'description': UnfoldAdminTextareaWidget(attrs={}),
            'tab': UnfoldAdminSelect(attrs={}),
            'filter': UnfoldAdminSelect(attrs={}),
            'catalog_page': UnfoldAdminSelect(attrs={}),
            'tag': UnfoldAdminSelect(attrs={}),
            'price_type': UnfoldAdminSelect(attrs={}),
            'runs': UnfoldBooleanWidget(attrs={}),
            'sale': UnfoldBooleanWidget(attrs={}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'name': UnfoldAdminTextInputWidget(attrs={}),
            'color': UnfoldAdminTextInputWidget(attrs={}),
        }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = '__all__'
        widgets = {
            'title': UnfoldAdminTextInputWidget(attrs={}),
            'type': UnfoldAdminSelect(attrs={}),
            'product': UnfoldAdminSelect(attrs={}),
        }


class SubFilterForm(forms.ModelForm):
    class Meta:
        model = SubFilter
        fields = '__all__'
        widgets = {
            'title': UnfoldAdminTextInputWidget(attrs={}),
            'price': UnfoldAdminDecimalFieldWidget(attrs={}),
        }


class SubFilterInline(TabularInline):
    model = SubFilter
    extra = 1
    form = SubFilterForm


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    form = FilterForm
    inlines = [
        SubFilterInline,
    ]


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
