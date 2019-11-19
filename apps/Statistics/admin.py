from django.contrib import admin

from apps.Statistics.models import Statistic, Feature


@admin.register(Statistic)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('command', 'count_queries',)
    ordering = ('-count_queries',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('text',)
