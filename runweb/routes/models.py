from django.db import models
from django.contrib.auth.models import User
from urllib.request import urlopen
from routes.polylines import Polyline

import json

class Route (models.Model):
    name = models.CharField(max_length = 128)
    roundtrip = models.BooleanField(default = False)
    distance = models.FloatField(default = 0.0)
    difficulty = models.FloatField(default = 0.0)
    owner = models.ForeignKey(User)
    
    def as_json(self):
        return {'name': self.name,
                'waypoints': [{'lat': wp.latitude, 'lng': wp.longitude} for wp in self.waypoint_set.all().order_by('index')],
                'distance': self.distance,
                'difficulty': self.difficulty,
                'round_trip': self.roundtrip}
                
    def get_directions(self):
        waypoints = list(self.waypoint_set.all().order_by('index')) # TODO: This might be inefficient, look into it later
        if len(waypoints) < 1:
            self.distance = 0.0
        else:
            if self.roundtrip:
                waypoints.append(waypoints[0])            
                
            url = 'https://maps.googleapis.com/maps/api/directions/json?'
            params = ['sensor=false',
                      'key=AIzaSyAzuJ-NRDmC66xWHKcyI5_BbZb5aRC9YtI',
                      'origin=' + waypoints[0].as_text(),
                      'destination=' + waypoints[-1].as_text(),
                      'avoid=highways|tolls',
                      'mode=walking',
                      'units=metric']

            if len(waypoints) > 2:
                params.append('waypoints=' + '|'.join([waypoints[i].as_text() for i in range(1, len(waypoints) - 1)]))
            url += '&'.join(params)

            # Inline call to google's direction API            
            data = json.loads(urlopen(url).read().decode('utf-8'))
            if data['status'] != 'OK':
                return None
            else:
                return data
                
    def calculate_distance(self):    
        data = self.get_directions()
        if data == None:
            self.distance = 0.0
        else:
            route = data['routes'][0]
            dist = 0.0
            for leg in route['legs']:
                dist += leg['distance']['value']
            self.distance = dist
        self.save()
		
    def get_polyline(self):
        data = self.get_directions()
        if data == None:
            return None
        else:
            return Polyline(data['routes'][0]['overview_polyline']['points'])
        

class Waypoint (models.Model):
    route = models.ForeignKey(Route)
    latitude = models.FloatField()
    longitude = models.FloatField()
    index = models.IntegerField()
    
    def as_text(self):
        return str(self.latitude) + ',' + str(self.longitude)
