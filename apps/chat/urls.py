from django.urls import re_path, path
from . import views

app_name = 'chat'

urlpatterns = [
    re_path(r'^$', views.user_list, name='index'),
    path("<str:room_name>/", views.room, name="room"),
]
