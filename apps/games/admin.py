from django.contrib import admin

from apps.games.models import Rate, Gamer, PetrovichUser, PetrovichGames


@admin.register(Gamer)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')


@admin.register(Rate)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat', 'rate')
    ordering = ('-chat',)


@admin.register(PetrovichUser)
class PetrovichUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat', 'wins', 'active',)
    list_filter = ('user', 'chat',)


@admin.register(PetrovichGames)
class PetrovichGamesAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'chat',)
    list_filter = ('user', 'chat',)
