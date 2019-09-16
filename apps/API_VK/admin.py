from django.contrib import admin

# Register your models here.
from apps.API_VK.models import TrustIMEI, VkChatId, Log, Stream, VkUser, Winners

admin.site.register(TrustIMEI)
admin.site.register(VkChatId)
admin.site.register(Stream)
admin.site.register(VkUser)


@admin.register(Winners)
class WinnersAdmin(admin.ModelAdmin):
    list_display = ('id', 'winner', 'date')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'imei', 'author', 'event', 'msg', 'success')
