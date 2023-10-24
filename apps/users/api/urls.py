from .views import UserDetailViewSet, UserListViewSet, UserRegistrationView
from django.urls import path


# /api/users/
urlpatterns = [
    path('api/user/', UserListViewSet.as_view(), name='user-list'),  # List view
    path('api/user/<int:pk>/', UserDetailViewSet.as_view(), name='user-detail'),
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    
    
]