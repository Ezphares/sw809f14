from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    rating = models.IntegerField(default=1500)
    rd = models.IntegerField(default=350)
    last_match = models.DateField(default=None, null=True)


class Match(models.Model):
    winner = models.ForeignKey(Player, related_name='winner')
    loser = models.ForeignKey(Player, related_name='loser')
    date = models.DateField(auto_now_add=True)
