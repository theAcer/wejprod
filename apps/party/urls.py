from django.urls import path
from . import views

app_name = 'party'

urlpatterns = [
  
    #party 
    # Party URLs
    path('create/<int:tournament_pk>/', views.PartyCreateView.as_view(), name='party_create'),
    path('update/<int:pk>/', views.PartyUpdateView.as_view(), name='party_update'),
    path('details/<int:pk>/', views.PartyDetailView.as_view(), name='party_details'),

    path('parties/', views.PartyListView.as_view(), name='party_list'),
    path('<int:pk>/', views.PartyDetailView.as_view(), name='party_detail'),
    path('join/<int:party_pk>/', views.JoinPartyView.as_view(), name='join_party'),
    path('leave/<int:party_pk>/', views.LeavePartyView.as_view(), name='leave_party'),
    # URL pattern for closing a party
    path('close/<int:pk>/', views.ClosePartyView.as_view(), name='close_party'),


    # Delete an existing party
    path('delete/<int:pk>/', views.PartyDeleteView.as_view(), name='party_delete'),
]
