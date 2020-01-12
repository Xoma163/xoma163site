from django.urls import path

from . import views

urlpatterns = [
    path('whereisme/', views.where_is_me),
    path('', views.petrovich),
    # url(r'^add_words/$', views.add_new_words, name='add words'),
]
