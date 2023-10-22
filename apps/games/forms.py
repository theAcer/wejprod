# forms.py

from django import forms
from .models import Score

class GameScoreForm(forms.Form):
    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game')
        super(GameScoreForm, self).__init__(*args, **kwargs)
        holes = game.tournament.course.hole_set.all()
        players = game.players.all()

        # Initialize the form fields with previous score values
        for player in players:
            for hole in holes:
                field_name = f'score_{player.id}_{hole.hole_number}'
                score = game.get_score_for_player_and_hole(player, hole.hole_number)
                initial_value = score.score if score else None
                self.fields[field_name] = forms.IntegerField(
                    required=False,
                    initial=initial_value,
                    widget=forms.NumberInput(attrs={'class': 'score-input'}),
                )