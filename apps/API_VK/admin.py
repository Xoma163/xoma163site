from django.contrib import admin

# Register your models here.
from apps.API_VK.models import TrustIMEI, VkChatId, Log

admin.site.register(TrustIMEI)
admin.site.register(VkChatId)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date', 'imei', 'author', 'event', 'msg', 'success')
