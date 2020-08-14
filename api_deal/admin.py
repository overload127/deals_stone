from django.contrib import admin
from .models import Gem, Customer, Deal


class DealInline(admin.TabularInline):
    """Отображение сделок в виде таблицы"""
    model = Deal
    extra = 1
    readonly_fields = ['__str__']


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    """Камни"""
    list_display = ['title']
    search_fields = ['title']
    inlines = [DealInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Участници сделок"""
    list_display = ['name']
    search_fields = ['name']
    inlines = [DealInline]


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """Сделки"""
    list_display = ['client', 'gem', 'total', 'quantity', 'date']
    search_fields = ['client__name', 'gem__title']
