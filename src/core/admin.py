from django.contrib import admin

from src.core.models import Setting, Subscriber, PromoCode


# Register your models here.

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'from_date', 'until_date', 'discount')  # Customize the display fields if needed
    exclude = ('users',)
