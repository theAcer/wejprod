from django.views.generic import DetailView
from .models import Game, Score
from .forms import GameScoreForm
from django.views.generic import FormView, CreateView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from silk.profiling.profiler import silk_profile


# Create a mixin with the profile decorator
class GameDetailViewMixin:
    @silk_profile(name='Game Detail View Profile')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

# Create a mixin with the profile decorator
class ScoreDetailViewMixin:
    @silk_profile(name='Score Detail View Profile')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
# Create a mixin with the profile decorator
class ScoreUploadViewMixin:
    @silk_profile(name='Score Upload View Profile')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class GameDetailView(GameDetailViewMixin, DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        scores_data = self.get_scores_for_hole_and_player(game)

        hole_numbers_str = game.hole_numbers
        hole_numbers = [int(num) for num in hole_numbers_str.split(',') if num.strip().isdigit()]
        context = {
            'scores_data': scores_data,
            'players': game.players,
            'game': game,
            'hole_numbers': hole_numbers
        }
        return context

    def get_scores_for_hole_and_player(self, game):
        # Logic to fetch scores for all holes and players in the game
        # You can use the game object to retrieve scores and organize the data
        # For example, you can use the game object's related manager to get scores:
        scores = game.score_set.select_related('hole', 'player').all()

        # Organize the data into a dictionary with player names as keys and
        # their scores for each hole as values
        scores_data = {}
        for score in scores:
            hole_number = score.hole.hole_number
            player_name = score.player.name
            score_id = score.pk
            score_value = score.score

            if player_name not in scores_data:
                # Store scores as tuples with None as default value
                scores_data[player_name] = (None,) * 9

            # Replace the None with the actual score for the hole
            scores_data[player_name] = tuple(score_value if idx + 1 == hole_number else value
                                            for idx, value in enumerate(scores_data[player_name]))


        return scores_data


class GameScoreUpdateView(FormView):
    template_name = 'games/game_scores.html'
    form_class = GameScoreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = get_object_or_404(Game, pk=self.kwargs['pk'])
        context['game'] = game
        context['players'] = game.players.all()
        context['holes'] = game.tournament.course.hole_set.all()
        context['scores_data'] = game.get_scores_data()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        game_pk = self.kwargs['pk']
        game = get_object_or_404(Game, pk=game_pk)
        kwargs['game'] = game
        return kwargs

    def form_valid(self, form):
        game_pk = self.kwargs['pk']
        game = get_object_or_404(Game, pk=game_pk)
        players = game.players.all()
        holes = game.tournament.course.hole_set.all()

        for player in players:
            for hole in holes:
                field_name = f'score_{player.id}_{hole.hole_number}' 
                score_value = form.cleaned_data.get(field_name) 
                score = game.get_score_for_player_and_hole(player, hole.hole_number)
                if score_value is not None:
                    if score:
                        score.score = score_value
                        score.save()
                    else:
                        # If no score exists for this player and hole, create a new score
                        Score.objects.create(game=game, player=player, hole=hole, score=score_value)
                elif score:
                    # If the score_value is None (empty input), delete the existing score
                    pass

        return redirect('games:game_detail', pk=game_pk)

    def get_success_url(self):
        return reverse('games:game_detail', kwargs={'pk': self.kwargs['pk']})


class ScoreUploadView(ScoreUploadViewMixin, FormView):
    form_class = GameScoreForm
    template_name = 'games/game_scores.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        game_id = self.kwargs['pk']
        game = get_object_or_404(Game, pk=game_id)
        score_id = self.kwargs['score_id']
        score = get_object_or_404(Score, pk=score_id)
        kwargs['game'] = game
        kwargs['instance'] = score  # Pass the Score instance to the form for updating
        return kwargs

    def form_valid(self, form):
        # Save the updated score
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Get the game ID from the URL parameters
        game_id = self.kwargs['pk']
        # Return the URL to the game detail page using reverse_lazy
        return reverse_lazy('games:game_detail', kwargs={'pk': game_id})