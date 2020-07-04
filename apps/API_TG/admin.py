from django.contrib import admin

# Register your models here.
from apps.API_TG.models import TgUser, TgTempUser

admin.site.register(TgUser)
admin.site.register(TgTempUser)
