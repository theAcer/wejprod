from django.db import models
from django.core.exceptions import ValidationError
from tournaments.models import Tournament
from users.models import Player


# Create your models here.
class Party(models.Model):
    players = models.ManyToManyField(Player, related_name='parties', blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    is_full = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    creator = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)  

    def is_party_closed(self):
        participants = self.party_participants.all()
        return all(participant.status == 'confirmed' for participant in participants)

    def __str__(self):
        return f"Party for {self.tournament.name} - Game Type: {self.tournament.game_type}"
    

class PartyParticipant(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'confirmed'),
        ('declined', 'declined'),
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.player.name} in {self.party} - Status: {self.get_status_display()}"
    

       