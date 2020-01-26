from django.urls import path

from apps.web import views, api

urlpatterns = [
    path('', views.index),
    path('calc/', views.calc),
    path('calc/<int:session_id>', views.calc_session),

    path('calc/add_row', api.add_row),
    path('calc/del_row', api.del_row),
    path('calc/save_rows', api.save_rows),

    path('calc/add_user', api.add_user),
    path('calc/del_user', api.del_user),
    path('calc/save_users', api.save_users),

    path('calc/get_calculate', api.get_calculate),

    path('chat/', views.chat)
]
