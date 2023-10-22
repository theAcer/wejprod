from django.contrib import admin
from .models import Tournament, Invitation, \
PlayerParticipation
# Register your models here.
admin.site.register(Tournament)
admin.site.register(Invitation)
admin.site.register(PlayerParticipation)