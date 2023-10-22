from django.contrib import admin
from .models import Game, Score, Hole
# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'start_time', 'party', 'hole_numbers','players' )
    filter_horizontal = ('players',)

admin.site.register(Game)

admin.site.register(Score)
admin.site.register(Hole)
