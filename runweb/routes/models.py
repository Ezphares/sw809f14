from django.db import models
from django.contrib.auth.models import User

class Route (models.Model):
    name = models.CharField(max_length = 128)
    owner = models.ForeignKey(User)

class Waypoint (models.Model):
    route = models.ForeignKey(Route)
    index = models.IntegerField()
