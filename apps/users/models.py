# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


def player_profile_picture_path(instance, filename):
    # Function to define the upload path for player profile pictures
    return f"profile_pictures/{instance.user.username}/{filename}"


class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    handicap = models.IntegerField()
    profile_picture = models.ImageField(upload_to=player_profile_picture_path, blank=True, null=True)
    # Add additional fields as needed

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('users:profile')