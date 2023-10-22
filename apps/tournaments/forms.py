from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Invitation, Player, Tournament


class TournamentForm(forms.ModelForm):
    HOLE_SELECTION_CHOICES = [
        ('full18', 'Full 18'),
        ('front9', 'Front 9'),
        ('back9', 'Back 9'),
        ('custom', 'Custom'),
    ]

    hole_selection = forms.ChoiceField(choices=HOLE_SELECTION_CHOICES)
    custom_holes = forms.CharField(required=False)

    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'course', 'game_type', 'hole_selection', 'custom_holes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['custom_holes'].widget = forms.TextInput(attrs={'placeholder': 'Enter custom hole numbers'})

    def clean(self):
        cleaned_data = super().clean()
        hole_selection = cleaned_data.get('hole_selection')
        custom_holes = cleaned_data.get('custom_holes')

        if hole_selection == 'custom' and not custom_holes:
            raise forms.ValidationError("Please provide a custom list of holes.")
        return cleaned_data

    def clean_custom_holes(self):
        hole_selection = self.cleaned_data.get('hole_selection')
        custom_holes = self.cleaned_data.get('custom_holes')

        if hole_selection == 'full18':
            # Get all hole numbers for an 18-hole course
            course = self.cleaned_data.get('course')
            if course:
                full_18_holes = [str(hole.hole_number) for hole in course.hole_set.all()]
                return ','.join(full_18_holes)

        elif hole_selection == 'front9':
            # Get the front 9 hole numbers for an 18-hole course
            course = self.cleaned_data.get('course')
            if course:
                front_9_holes = [str(hole.hole_number) for hole in course.hole_set.filter(hole_number__lte=9)]
                return ','.join(front_9_holes)

        elif hole_selection == 'back9':
            # Get the back 9 hole numbers for an 18-hole course
            course = self.cleaned_data.get('course')
            if course:
                back_9_holes = [str(hole.hole_number) for hole in course.hole_set.filter(hole_number__gte=10)]
                return ','.join(back_9_holes)

        # For other options or custom holes, return the value as is
        return custom_holes

class InvitationForm(forms.ModelForm):
    def __init__(self, creator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["invited_players"].queryset = Player.objects.exclude(id=creator.id)

    class Meta:
        model = Invitation
        fields = ['invited_players', 'status']
        labels = {'invited_players': 'select players to invite'}

class JoinTournamentForm(forms.Form):
    # The form can have a submit button field to allow users to join the tournament.
    join_button = forms.CharField(widget=forms.HiddenInput(), initial='join', required=False)