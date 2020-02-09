from django.contrib import admin

# Register your models here.
from apps.API_VK.models import Log, VkUser, QuoteBook, VkBot, VkChat, Words


@admin.register(VkUser)
class VkUserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'name', 'surname', 'nickname', 'nickname_real', 'gender', 'birthday', 'city',
        # 'is_admin', 'is_moderator', 'is_student', 'is_banned', 'is_minecraft', 'is_terraria'
    )
    list_filter = (
        'gender', 'city', 'groups',
        # 'is_admin', 'is_moderator', 'is_student', 'is_banned', 'city', 'is_minecraft', 'is_terraria')
    )


@admin.register(VkChat)
class VkChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'name',)


@admin.register(VkBot)
class VkBotAdmin(admin.ModelAdmin):
    list_display = ('bot_id', 'name',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    list_display = ('date', 'imei', 'author', 'event', 'msg', 'success')
    list_filter = ('author',)


@admin.register(QuoteBook)
class QuoteBookAdmin(admin.ModelAdmin):
    list_display = ('peer_id', 'date', 'text')
    list_filter = ('peer_id',)


@admin.register(Words)
class WordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'm1', 'f1', 'n1', 'mm', 'fm', 'type')
    list_filter = ('type',)
    search_fields = ['id', 'm1', 'f1', 'n1', 'mm', 'fm', 'type']
