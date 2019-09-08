from django.contrib import admin

# Register your models here.
from apps.API.models import TelegramTrustIMEI, TelegramChatId, Log

admin.site.register(TelegramTrustIMEI)
admin.site.register(TelegramChatId)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date', 'imei', 'author', 'event', 'msg', 'success')
