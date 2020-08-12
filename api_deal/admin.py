from django.contrib import admin
from .models import Gem, Client


class ClientInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Client.gems.through
    extra = 1
    readonly_fields = ['__str__']


class GemInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Gem.owners.through
    extra = 1
    readonly_fields = ['__str__']


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ['title']
    search_fields = ['title']
    inlines = [ClientInline]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ['username']
    search_fields = ['username']
    inlines = [GemInline]
