from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key = True)
    rating = models.IntegerField(default = 1500)
    rd = models.IntegerField(default = 350)

class Matches(models.Model):
    player1 = models.ForeignKey(Profile, related_name = 'player_1')
    player2 = models.ForeignKey(Profile, related_name = 'player_2')
    # Result: 1: player 1 wins, 0: player 2 wins, 0.5: draw	
    result = models.FloatField()
    date = models.DateField(auto_now_add = True)
