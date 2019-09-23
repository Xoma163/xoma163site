from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^whereisme/$', views.where_is_me, name='where_is_me'),
]
