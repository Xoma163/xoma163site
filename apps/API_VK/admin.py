from django.contrib import admin

# Register your models here.
from apps.API_VK.models import Log, StreamModel, VkUser, QuoteBook, PetrovichUser, PetrovichGames, VkBot, VkChat

admin.site.register(StreamModel)


@admin.register(VkUser)
class VkUserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'name', 'surname', 'nickname', 'gender', 'birthday', 'city', 'get_notify_from', 'send_notify',
        'is_admin', 'is_moderator', 'is_student', 'is_banned')
    list_filter = ('gender', 'send_notify', 'is_admin', 'is_moderator', 'is_student', 'is_banned', 'city')


@admin.register(VkChat)
class VkChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'name',)


@admin.register(VkBot)
class VkBotAdmin(admin.ModelAdmin):
    list_display = ('bot_id', 'name',)


@admin.register(PetrovichUser)
class PetrovichUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat', 'wins',)
    list_filter = ('user', 'chat',)


@admin.register(PetrovichGames)
class PetrovichGamesAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'chat',)
    list_filter = ('user', 'chat',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    list_display = ('id', 'date', 'imei', 'author', 'event', 'msg', 'success')
    list_filter = ('author',)


@admin.register(QuoteBook)
class QuoteBookAdmin(admin.ModelAdmin):
    readonly_fields = ('peer_id', 'date', 'text')
    list_display = ('peer_id', 'date', 'text')
    list_filter = ('peer_id',)
