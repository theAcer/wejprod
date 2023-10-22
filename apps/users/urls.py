# users/urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import SignupPageView, PlayerProfileView, \
    PlayerProfileUpdateView
#from azureproject.urls import schema_view



app_name = 'users'



urlpatterns = [
    path('', include('users.api.urls')),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('profile/', PlayerProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', PlayerProfileUpdateView.as_view(),\
          name='player_profile_update'),
    #path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]