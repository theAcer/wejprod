from django.urls import path
from .views import GameDetailView, GameScoreUpdateView


app_name = 'games'

urlpatterns = [
    path('<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    # Add other URLs for create, update, delete, list views, etc.
     # Other URL patterns for your app...
    #path('score/<int:pk>', GameScoreView.as_view(), name='game_score'),

    path('<int:pk>/update-scores/', GameScoreUpdateView.as_view(), name='game_scores'),
]