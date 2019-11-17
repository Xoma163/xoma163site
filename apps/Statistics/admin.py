from django.contrib import admin

from apps.Statistics.models import Statistics


@admin.register(Statistics)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('command', 'count_queries',)
    ordering = ('-count_queries',)
