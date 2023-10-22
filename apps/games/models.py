from django.db import models
from django.urls import reverse

from courses.models import Course
from tournaments.models import Tournament
from users.models import Player
from party.models import Party


class Game(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='games', null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    # date = models.DateTimeField()
    players = models.ManyToManyField(Player, related_name='games')
    # game_type = models.CharField(max_length=50)
    start_time = models.TimeField(null=True, blank=True)

    hole_numbers = models.CharField(max_length=100, blank=True, null=True)
    # end_time = models.TimeField(null=True, blank=True)
    # weather_conditions = models.CharField(max_length=100, null=True, blank=True)
    # winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    # notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Game on {self.start_time}'

    def save(self, *args, **kwargs):
        creating_new_game = not self.pk  # Check if the game is being created or updated
        super().save(*args, **kwargs)
        
        if creating_new_game:
            hole_numbers = [int(hole_number) for hole_number in self.hole_numbers.split(",") if hole_number.strip()]
            players = self.players.all()

            for player in players:
                for hole_number in hole_numbers:
                    # Assuming you want to initialize all scores to 0
                    ScoreFactory.create_score(self, player, hole_number, 0)


    def update_score(self, score_id, score_value):
        # Update the score value for a given score_id
        try:
            score = Score.objects.get(id=score_id, game=self)
            score.score = score_value
            score.save()
            return score
        except Score.DoesNotExist:
            return None
        
    def get_scores_for_player(self, player):
        # Get all scores for a specific player in this game
        return Score.objects.filter(game=self, player=player)

    def get_scores_for_hole(self, hole_number):
        # Get all scores for a specific hole in this game
        hole = Hole.objects.get(course=self.tournament.course, hole_number=hole_number)
        return Score.objects.filter(game=self, hole=hole)

    def get_score_for_player_and_hole(self, player, hole_number):
        # Get the score for a specific player and hole in this game
        
        try:
            return Score.objects.get(game=self, player=player, hole__hole_number=hole_number)
        except Score.DoesNotExist:
            return None
        
    def get_scores_data(self):
        scores_data = {}
        for score in self.score_set.all():
            player_name = score.player.name
            hole_number = score.hole.hole_number
            score_value = score.score

            if player_name not in scores_data:
                scores_data[player_name] = {}

            scores_data[player_name][hole_number] = score_value

        return scores_data

    def get_absolute_url(self):
        return reverse('games:game_detail', kwargs={'pk': self.pk})


class Hole(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    hole_number = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=10)
    par = models.PositiveIntegerField()
    yardage = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.name}, Hole {self.hole_number}, Par {self.par}"
        

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.name} - Tournament: {self.tournament.name}, Score: {self.score}, Hole: {self.hole.hole_number}"


class ScoreFactory:
    
    def create_game_and_scores(self, party):
        game_type = party.tournament.hole_selection
        holes = self.get_holes_for_game_type(game_type)

        # Create a new game for the closed party
        game = Game.objects.create(
            party=party,
            start_time=party.start_time,
            hole_numbers=holes,
            tournament=party.tournament,
        )

        # Initialize players in the game from the party participants
        participants = party.partyparticipant_set.filter(status='confirmed')
        players = [participant.player for participant in participants]
        game.players.set(players)

        # Create Score objects for each player and hole in the game
        tournament = party.tournament
        for hole_number in holes.split(','):
            hole = Hole.objects.get(course=party.tournament.course, hole_number=int(hole_number))
            for player in players:
                score = Score.objects.create(game=game, tournament=tournament, player=player, hole=hole, score=None)

    def get_holes_for_game_type(self, game_type):
        if game_type == '18':
            return '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18'  # Assuming a full 18-hole course
        elif game_type == 'F9':
            return '1,2,3,4,5,6,7,8,9'  # Assuming front 9 holes
        elif game_type == 'B9':
            return '10,11,12,13,14,15,16,17,18'  # Assuming Back 9 holes
        elif game_type == 'custom':
            # Get the custom holes from the tournament (assuming you have stored them as a comma-separated string)
            return game_type.custom_holes  # Replace 'custom_holes' with the actual field name you use to store custom holes
        else:
            # Handle other game types here if needed
            return ''
