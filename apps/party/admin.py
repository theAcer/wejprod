from django.contrib import admin
from .models import Party, PartyParticipant
# Register your models here.
admin.site.register(Party)
admin.site.register(PartyParticipant)