from django.contrib import admin

from apps.Statistics.models import Statistic, Issue, Service, Counter


@admin.register(Statistic)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('command', 'count_queries',)
    ordering = ('-count_queries',)


@admin.register(Issue)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('text',)


admin.site.register(Service)


@admin.register(Counter)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'chat')
