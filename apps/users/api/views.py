from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer 
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser, Player
from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.response import Response
from apps.firebase_auth.authentication import FirebaseAuthentication  # Import your FirebaseAuthentication class
from firebase_admin import auth
from rest_framework.decorators import api_view, authentication_classes



class UserDetailViewSet(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Make sure the user is authenticated
    #authentication_classes = [] 
    
    def get_object(self):
        return self.request.user 