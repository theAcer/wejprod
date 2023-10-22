# forms.py
from django import forms
from .models import Party
from django.forms import ModelMultipleChoiceField
from tournaments.models import Tournament

class PartyForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Party
        fields = ['is_full', 'is_closed', 'players']

    def __init__(self, *args, tournament=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tournament = tournament
        # Set the queryset for the players field to the participants of the tournament
        if tournament:
            self.fields['players'].queryset = tournament.participants.all()

    def save(self, commit=True):
        party = super().save(commit=False)
        party.tournament = self.tournament
        if commit:
            party.save()
            self.save_m2m()  # Save many-to-many relationships (players)
        return party
    
class ClosePartyForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        widget=forms.HiddenInput(),  # Hidden field, the value will be True by default
        initial=True,
    )