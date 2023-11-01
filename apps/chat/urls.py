from django.contrib import admin
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.user_list, name='chat'),
]