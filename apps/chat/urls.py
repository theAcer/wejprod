from django.urls import re_path, path
from . import views

app_name = 'chat'

urlpatterns = [
    re_path(r'^$', views.user_list, name='index'),
    path('room/<str:room_name>/', views.course_chat_room,
         name='course_chat_room'),
]
