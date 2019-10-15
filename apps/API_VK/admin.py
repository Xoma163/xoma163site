from django.contrib import admin

# Register your models here.
from apps.API_VK.models import TrustIMEI, VkChatId, Log, Stream, VkUser, Winners, QuoteBook

admin.site.register(TrustIMEI)


@admin.register(VkChatId)
class VkChatIdAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id', 'is_active', 'is_admin')


admin.site.register(Stream)


@admin.register(VkUser)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'chat_id', 'user_id')


@admin.register(Winners)
class WinnersAdmin(admin.ModelAdmin):
    list_display = ('id', 'winner', 'date')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    list_display = ('id', 'date', 'imei', 'author', 'event', 'msg', 'success')


@admin.register(QuoteBook)
class QuoteBookAdmin(admin.ModelAdmin):
    readonly_fields = ('text', 'date', 'username', 'user_id', 'peer_id')
