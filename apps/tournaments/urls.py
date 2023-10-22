from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    
    path('', views.TournamentListView.as_view(), name='tournament_list'),
    path('create/', views.TournamentCreateView.as_view(), name='tournament_create'),
    path('<int:pk>/', views.TournamentDetailView.as_view(), name='tournament_detail'),
    path('<int:pk>/invitation/', views.TournamentInvitationView.as_view(), name='tournament_invitation'),
    path('join/<int:pk>/', views.JoinTournamentView.as_view(), name='join_tournament'),
    path('exit/<int:pk>/', views.ExitTournamentView.as_view(), name='exit_tournament'),

    #invitations
    path('invitations/', views.InvitationListView.as_view(), name='invitation_list'),
    path('invitations/<int:pk>/', views.InvitationDetailView.as_view(), name='invitation_detail'),
     # Accept invitation
    path('invitation/accept/<int:invitation_id>/', views.AcceptInvitationView.as_view(), name='accept_invitation'),

    # Decline invitation
    path('invitation/decline/<int:invitation_id>/', views.DeclineInvitationView.as_view(), name='decline_invitation'),

  
]
