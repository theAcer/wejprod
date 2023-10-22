from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Player


@receiver(post_save, sender=CustomUser)
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance, name=instance.username, handicap=0)