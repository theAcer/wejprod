from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import FormView, DeleteView, UpdateView,\
      ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.base import RedirectView
from django.contrib import messages

from .models import Party, PartyParticipant
from tournaments.models import Tournament
from .forms import PartyForm
from games.models import ScoreFactory


class PartyCreateView(CreateView):
    model = Party
    form_class = PartyForm
    template_name = 'party/party_create.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        tournament = get_object_or_404(Tournament, pk=self.kwargs['tournament_pk'])
        kwargs['tournament'] = tournament
        return kwargs
    
    def form_valid(self, form):
        tournament = get_object_or_404(Tournament, pk=self.kwargs['tournament_pk'])
        form.instance.tournament = tournament
        # Set the user as the creator of the party
        form.instance.creator = self.request.user.player

        # Save the party instance
        self.object = form.save()

        participants = form.cleaned_data['players']
        for participant in participants:
            PartyParticipant.objects.create(party=self.object, player=participant)


        return super().form_valid(form)

    def get_success_url(self):
        tournament = get_object_or_404(Tournament, pk=self.kwargs['tournament_pk'])
        return reverse_lazy('tournaments:tournament_detail', kwargs={'pk': tournament.pk})
    

class PartyUpdateView(UpdateView):
    model = Party
    template_name = 'party/party_update.html'
    fields = ['name', 'players']
    success_url = reverse_lazy('party:party_list')

class PartyDeleteView(DeleteView):
    model = Party
    template_name = 'party/party_confirm_delete.html'
    success_url = reverse_lazy('party:party_list')

class PartyDetailView(DetailView):
    model = Party
    template_name = 'party/party_details.html'
    context_object_name = 'party'

    def get_queryset(self):
        # Filter the queryset to include only parties that are full or closed
        return Party.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        party = self.get_object()
        # Check if the current user is a participant in the party
        context['user_is_party_participant'] = party.players.filter(id=self.request.user.player.id).exists()

        # Check if the current user is the creator of the party
        context['user_is_party_creator'] = self.object.creator == self.request.user.player
        
        # Add additional context data here if needed
        
        return context
    
    def post(self, request, *args, **kwargs):
        party = self.get_object()
        user = request.user
        action = request.POST.get('action')

        if action == 'join':
            # ... your existing join party logic ...
            pass

        elif action == 'leave':
            # ... your existing leave party logic ...
            pass

        elif action == 'agree':
            participant = party.party_participants.get(player=user.player)
            participant.status = 'confirmed'
            participant.save()

            if party.is_party_closed():
                # Party is now closed, add any additional logic here
                pass

        return redirect('tournaments:party_detail', pk=party.pk)

class PartyListView(ListView):
    model = Party
    template_name = 'party/party_list.html'
    context_object_name = 'parties'

class JoinPartyView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs['party_pk'])
        user = self.request.user

        # Check if the current user is not already a participant
        if not party.players.filter(id=user.player.id).exists():
            # Add the current user to the party's players
            party.players.add(user.player)

        # Return the URL to redirect after joining the party
        return reverse('party:party_detail', kwargs={'pk': party.pk})
    
    
class LeavePartyView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        party_pk = self.kwargs['party_pk']
        party = get_object_or_404(Party, pk=party_pk)
        user = self.request.user

        # Check if the user is a participant before removing them
        if party.players.filter(id=user.player.id).exists():
            party.players.remove(user.player)
            print(f'player{user.player.name} has left the party')
        else:
            # User is not a participant, handle the error accordingly
            # For example, you can redirect them to an error page or display a message.
            # Here, we will redirect them to the party detail page.
            print(f'player{user.player.name} was not a participant')
            return reverse('party:party_detail', kwargs={'pk': party.pk})

        # Return the URL to redirect after leaving the party

        return reverse('party:party_detail', kwargs={'pk': party.pk})
    


class ClosePartyView(View):
    def get_party(self, pk):
        return get_object_or_404(Party, pk=pk)

    def post(self, request, pk):
        party = self.get_party(pk)

        # Check if the current user is the creator of the party
        if party.creator != request.user.player:
            # Redirect with an error message if the user is not the creator
            messages.error(request, "You are not the creator of this party.")
            return redirect('party:party_detail', pk=party.pk)

        # Check if all participants have confirmed the party
        participants = PartyParticipant.objects.filter(party=party)
        if not all(participant.status == 'confirmed' for participant in participants):
            messages.error(request, "All participants must confirm the party before closing.")
            return redirect('party:party_detail', pk=party.pk)

        # Update the party status to 'closed' and save
        party.is_closed = True
        party.save()

        # Create an instance of ScoreFactory
        score_factory = ScoreFactory()

        # Call the instance method create_game_and_scores on the score_factory instance
        score_factory.create_game_and_scores(party)

        # Send confirmation notifications to all participants (optional)
        for participant in participants:
            # You can add your notification logic here to send confirmations
            print(f'confirmation sent to {participant.player.name}')

        # Redirect with a success message after closing the party
        messages.success(request, "The party has been closed successfully.")
        return redirect('party:party_detail', pk=party.pk)
    