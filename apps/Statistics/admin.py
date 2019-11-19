from django.contrib import admin

from apps.Statistics.models import Statistic, Isssue


@admin.register(Statistic)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('command', 'count_queries',)
    ordering = ('-count_queries',)


@admin.register(Isssue)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('text',)
