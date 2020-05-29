from django.contrib import admin

from apps.service.models import Statistic, Issue, Service, Counter, Cat, Meme, Notify, City, AudioList, LaterMessage, \
    Donations, TimeZone, LaterMessageSession, YoutubeSubscribe


@admin.register(Statistic)
class VkUserAdmin(admin.ModelAdmin):
    list_display = ('command', 'count_queries',)
    ordering = ('-count_queries',)


@admin.register(Issue)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('author', 'text',)


admin.site.register(Service)


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'chat')
    list_filter = (('chat', admin.RelatedOnlyFieldListFilter),)


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'preview', 'author', 'to_send')
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), 'to_send',)


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview_image', 'preview_link', 'author', 'approved', 'type', 'uses')
    search_fields = ['name', 'link']
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), 'type', 'approved')


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'text', 'author', 'chat', 'repeat')
    search_fields = ['date', 'text', 'text_for_filter']
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), ('chat', admin.RelatedOnlyFieldListFilter), 'repeat',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'synonyms', 'timezone', 'lat', 'lon')


@admin.register(TimeZone)
class TimeZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AudioList)
class AudioListAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'attachment')


@admin.register(Donations)
class DonationsAdmin(admin.ModelAdmin):
    list_display = ('username', 'amount', 'currency', 'message', 'date')


@admin.register(LaterMessage)
class LaterMessageAdmin(admin.ModelAdmin):
    list_display = ('message_author', 'message_bot', 'text', 'date', 'attachments')
    list_filter = (('message_author', admin.RelatedOnlyFieldListFilter),
                   ('message_bot', admin.RelatedOnlyFieldListFilter))


@admin.register(LaterMessageSession)
class LaterMessageSessionAdmin(admin.ModelAdmin):
    list_display = ('author', 'date')
    list_filter = (('author', admin.RelatedOnlyFieldListFilter),)


@admin.register(YoutubeSubscribe)
class YoutubeSubscribeAdmin(admin.ModelAdmin):
    list_display = ('author', 'chat', 'title', 'date',)
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), ('chat', admin.RelatedOnlyFieldListFilter),)
