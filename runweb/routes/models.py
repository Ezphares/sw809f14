from django.db import models
from django.contrib.auth.models import User
import json

class Route (models.Model):
    name = models.CharField(max_length = 128)
    roundtrip = models.BooleanField(default = False)
    owner = models.ForeignKey(User)
	
    def as_json(self):
        return {'name': self.name,
                'waypoints': [{'lat': wp.latitude, 'lng': wp.longitude} for wp in self.waypoint_set.all().order_by('index')],
				'round_trip': self.roundtrip}

class Waypoint (models.Model):
    route = models.ForeignKey(Route)
    latitude = models.FloatField()
    longitude = models.FloatField()
    index = models.IntegerField()
