from django.contrib import admin

from apps.games.models import Rate, Gamer


@admin.register(Gamer)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')


@admin.register(Rate)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat', 'rate')
    ordering = ('-chat',)
