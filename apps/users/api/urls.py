from .views import UserDetailViewSet 
from django.urls import path


# /api/users/
urlpatterns = [
    path('api/user/', UserDetailViewSet.as_view(), name='user-detail'),
    
]