# wagers/forms.py
from django import forms
from .models import Event, Participant

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'category']

class WagerForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    chosen_option = forms.ModelChoiceField(queryset=Participant.objects.all())
    stake_distribution = forms.CharField(widget=forms.Textarea)
