from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^whereisme/$', views.whereisme, name='whereisme'),

]
