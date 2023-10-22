from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, ListView, CreateView,\
      DetailView, RedirectView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from party.forms import PartyForm

from party.models import Party
from .models import Tournament, Invitation, PlayerParticipation
from .forms import InvitationForm, JoinTournamentForm, TournamentForm
from bootstrap_datepicker_plus.widgets import DatePickerInput


class TournamentListView(ListView):
    model = Tournament
    template_name = 'tournaments/tournament_list.html'
    context_object_name = 'tournaments'


class TournamentCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    template_name = 'tournaments/tournament_create.html'
    form_class = TournamentForm

    def get_form(self):
        form = super().get_form()
        form.fields["start_date"].widget = DatePickerInput()
        form.fields["end_date"].widget = DatePickerInput()
        
        return form
    
    def form_valid(self, form):
        # Save the tournament instance
        self.object = form.save(commit=False)
        self.object.creator = self.request.user.player
        self.object.save()

        # Create a new PlayerParticipation instance for the creator
        PlayerParticipation.objects.create(tournament=self.object, player=self.request.user.player)

        return super().form_valid(form)

    
    def get_success_url(self):
        return reverse_lazy('tournaments:tournament_detail', kwargs={'pk': self.object.pk})


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = 'tournaments/tournament_detail.html'
    context_object_name = 'tournament'


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('participants')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        participants = tournament.participants.all()
         # Include the PartyForm in the template context
        context['party_form'] = PartyForm(tournament=tournament)
        context['participants'] = participants
        # Check if the user is a participant in tournament
        context['user_is_participant'] = tournament.participants.filter(id=self.request.user.player.id).exists()
        # Check if the user is a participant in any party
        context['user_is_participant_in_any_party'] = Party.objects.filter(players__id=self.request.user.player.id).exists()
        # Get the associated parties for the tournament
        parties = tournament.party_set.all()
        context['parties'] = parties
        return context

    def post(self, request, *args, **kwargs):
        tournament = self.get_object()
        user = request.user
        action = request.POST.get('action')

        if action == 'join':
            # Check if the user is not already a participant
            if not tournament.players.filter(id=user.player.id).exists():
                tournament.players.add(user.player)
        elif action == 'leave':
            # Check if the user is a participant before removing them
            if tournament.players.filter(id=user.player.id).exists():
                tournament.players.remove(user.player)
        return redirect('tournaments:tournament_detail', pk=tournament.pk)

class JoinTournamentView(FormView):
    template_name = 'tournaments/tournament_join.html'
    form_class = JoinTournamentForm

    def get_success_url(self):
        tournament = self.get_tournament()
        return reverse_lazy('tournaments:tournament_detail', kwargs={'pk': tournament.pk})
    
    def get_tournament(self):
        return get_object_or_404(Tournament, pk=self.kwargs['pk'])

    def form_valid(self, form):
        tournament = self.get_tournament()

        # Check if the user is not already a participant in the tournament
        if not tournament.participants.filter(id=self.request.user.player.id).exists():
            tournament.participants.add(self.request.user.player)
            # Add any additional logic here, such as sending a confirmation email, etc.

        return super().form_valid(form)


class ExitTournamentView(RedirectView):
    permanent = False
    pattern_name = 'tournaments:tournament_detail'

    def get_redirect_url(self, *args, **kwargs):
        tournament = get_object_or_404(Tournament, pk=self.kwargs['pk'])
        user = self.request.user

        # Check if the user is a participant before removing them
        if tournament.participants.filter(id=user.player.id).exists():
            tournament.participants.remove(user.player)

            # Remove the player from the party if they are in it
            party = tournament.party_set.filter(players=user.player).first()
            if party:
                party.players.remove(user.player)

            messages.success(self.request, "You have exited the tournament.")
        else:
            messages.error(self.request, "You are not a participant in this tournament.")

        return super().get_redirect_url(*args, **kwargs)    
    

class TournamentInvitationView(LoginRequiredMixin, FormView):
    template_name = 'tournaments/tournament_invitation.html'
    form_class = InvitationForm
    
    def get_tournament(self):
        tournament_pk = self.kwargs['pk']
        return get_object_or_404(Tournament, pk=tournament_pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.get_tournament()
        return context
    
    def form_valid(self, form):
        tournament = self.get_tournament()
        invited_players = form.cleaned_data['invited_players']
        creator_player = self.request.user.player

        print("Tournament:", tournament)
        print("Invited Players:", invited_players)
        print("Creator Player:", creator_player)

        # Check if the current user is a participant in any game of the tournament
        #if not tournament.game_set.filter(players=creator_player).exists():
            #print("Current user is not a participant in any game of the tournament.")
            #return redirect('tournaments:tournament_detail', pk=tournament.pk)

        # Create the invitation and associate it with the tournament
        invitation = Invitation.objects.create(tournament=tournament, status='pending')
        # Add the invited players to the invitation
        invitation.invited_players.set(invited_players)
        invitation.save()

        print("Invitation created successfully!")

        return redirect('tournaments:tournament_detail', pk=tournament.pk)

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['creator'] = self.request.user.player
        return kwargs
    

class InvitationListView(LoginRequiredMixin, ListView):
    model = Invitation
    template_name = 'tournaments/invitation_list.html'
    context_object_name = 'invitations'

    def get_queryset(self):
        player = self.request.user.player
        return Invitation.objects.filter(invited_players=player, status='pending')
    
class AcceptInvitationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        invitation = get_object_or_404(Invitation, id=self.kwargs['invitation_id'])
        # Handle the logic for accepting the invitation
        invitation.status = 'accepted'
        invitation.save()
        #Join tournament
        tournament = self.get_tournament()

        # Check if the user is not already a participant in the tournament
        if not tournament.participants.filter(id=self.request.user.player.id).exists():
            tournament.participants.add(self.request.user.player)
            # Add any additional logic here, such as sending a confirmation email, etc.
        return reverse('tournaments:invitation_detail', kwargs={'pk': invitation.pk})


class DeclineInvitationView(RedirectView):
    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        invitation = get_object_or_404(Invitation, id=self.kwargs['invitation_id'])
        # Handle the logic for declining the invitation
        invitation.status = 'declined'
        invitation.save()
        return reverse('tournaments:invitation_detail', kwargs={'pk': invitation.pk})
    

class InvitationDetailView(DetailView):
    model = Invitation
    template_name = 'tournaments/invitation_detail.html'
    context_object_name = 'invitation'

