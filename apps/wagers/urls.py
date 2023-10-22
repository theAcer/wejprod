# wagers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('place_wager/<int:pk>/', views.PlaceWagerView.as_view(), name='place_wager'),
    path('create_event/', views.EventCreateView.as_view(), name='create_event'),

]
