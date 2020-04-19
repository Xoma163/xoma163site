from django.contrib import admin

from apps.service.models import Statistic, Issue, Service, Counter, Cat, Meme, Notify, City, AudioList, LaterMessage


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


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'preview', 'author')


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'preview', 'author')
    search_fields = ['name', 'link']
    list_filter = (('author', admin.RelatedOnlyFieldListFilter),)


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'text', 'author', 'chat', 'repeat')
    search_fields = ['date', 'text', 'text_for_filter']
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), ('chat', admin.RelatedOnlyFieldListFilter), 'repeat',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'synonyms', 'timezone', 'lat', 'lon')


@admin.register(AudioList)
class AudioListAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'attachment')


@admin.register(LaterMessage)
class LaterMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'message_author', 'text', 'date', 'attachments')
