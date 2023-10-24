from rest_framework import viewsets, status, permissions
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
from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Open for anyone

    def perform_create(self, serializer):
        user = serializer.save()

        # If you want to customize additional actions or authentication, you can do it here

        # Log the user in using Django's login function
        login(self.request, user)

class UserDetailViewSet(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Make sure the user is authenticated
    #authentication_classes = [] 
    
    def get_queryset(self):
        return self.request.user 


class UserListViewSet(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer