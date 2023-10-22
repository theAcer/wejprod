
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.models import Player
from courses.models import Course


class Tournament(models.Model):
    GAME_TYPE_CHOICES = (
    ('match play', 'match play'),
    ('stroke play', 'stroke play'),
    ('nassau', 'Nassau'),
    )
    HOLE_SELECTION_CHOICES = (
        ('18', '18'),
        ('F9', 'F9'),
        ('B9', 'Back 9'),
        ('custom', 'Custom'),
    )
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=50, choices=GAME_TYPE_CHOICES, default='stroke play')
    participants = models.ManyToManyField(Player, through='PlayerParticipation', related_name='participants')
    hole_selection = models.CharField(max_length=10, choices=HOLE_SELECTION_CHOICES, default='full 18')
    custom_holes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tournament_detail', args=[self.pk])
 
    # Other fields and methods specific to the tournament
 

class Invitation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    invited_players = models.ManyToManyField(Player)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    

    def __str__(self):
        return f"Invitation for Tournament: {self.tournament.name}"
    

class PlayerParticipation(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return f"Player: {self.player.name} - Tournament: {self.tournament.name}"
