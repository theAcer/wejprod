# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from .models import Player
from django.views.generic import DetailView, UpdateView


 # Import your FirebaseAuthentication class
from firebase_admin import auth  # Import Firebase's auth module


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        # Call the parent method to save the user in the Django database
        response = super().form_valid(form)

        # Get user email and password from the form
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        try:
            # Create the user in Firebase using email and password
            user = auth.create_user_with_email_and_password(email, password)
            # You can customize user data and perform additional actions here

            # Authenticate the user using Django's authentication system
            self.request.user = user

            # Log the user in using Django's login function
            login(self.request, user)

        except auth.AuthError as e:
            # Handle Firebase authentication error
            error_message = "An error occurred during registration. Please try again later."
            # You can customize the error message based on the specific error
            # For example, you can check e.detail for more details about the error

            # Add an error to the form's errors and return the form
            form.add_error(None, error_message)
            return self.form_invalid(form)

        # Return a redirect response to the success URL
        return redirect(self.success_url)
    
    
class PlayerProfileView(DetailView):
    model = Player
    template_name = 'player/player_profile.html'
    context_object_name = 'player'

    def get_object(self, queryset=None):
        # Retrieve the player object based on the currently authenticated user
        return self.request.user.player
    

class PlayerProfileUpdateView(UpdateView):
    model = Player
    template_name = 'player/player_profile_update.html'
    fields = ['name', 'handicap', 'profile_picture']
    # You can include additional fields as needed

    def get_object(self, queryset=None):
        # Retrieve the player object based on the logged-in user
        return self.request.user.player