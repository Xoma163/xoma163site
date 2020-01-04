from django.contrib import admin

from apps.web.models import Session, User, Tare, Product, Order

admin.site.register(Session)
admin.site.register(User)
admin.site.register(Tare)
admin.site.register(Product)
admin.site.register(Order)
