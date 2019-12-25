from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^whereisme/$', views.where_is_me),
    url(r'^petrovich/$', views.petrovich),
    # url(r'^add_words/$', views.add_new_words, name='add words'),
]
