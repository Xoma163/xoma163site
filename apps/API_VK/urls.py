from django.urls import path

from . import views

urlpatterns = [
    path('whereisme/', views.where_is_me),

    path('chat/', views.chat_api),
    path('', views.petrovich_api),
    # url(r'^add_words/$', views.add_new_words, name='add words'),
]
