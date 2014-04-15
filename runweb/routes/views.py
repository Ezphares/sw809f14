# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from routes.models import Route, Waypoint
import json

@login_required
def overview(request, as_json = False):
    if as_json:
        return HttpResponse(json.dumps({'routes': [route.as_json() for route in Route.objects.filter(owner = request.user)]})) 
    else:
	    return render(request, 'route_list.html', {'routes': Route.objects.filter(owner = request.user)})

		
@login_required
def delete(request, load):
    if (load):
        try:
            route = Route.objects.get(owner = request.user, pk = int(load))
        except:
            return render(request, 'route_list.html', {'error': 'Attempt to access invalid route', 'routes': Route.objects.filter(owner = request.user)})
			
    route.delete()
    return HttpResponseRedirect('/')

@login_required
def planner(request, load = None):
    route = None
    if (load):
        try:
            route = Route.objects.get(owner = request.user, pk = int(load))
        except:
            return render(request, 'route_list.html', {'error': 'Attempt to access invalid route'})

    if (request.method == 'GET'):
        data = {}
        if route:
            data['load_route'] = json.dumps(route.as_json())
        return render(request, 'routing.html', data)
    else:
        #TODO: 'Invalid data' responses should be more graceful
        try:
            data = json.loads(request.REQUEST.get('json', '{}'))
            if type (data) is not dict:
                return HttpResponse('Invalid data a')
        except:
            return HttpResponse('Invalid data b')

        if not route:
            route = Route(owner = request.user)

        #Round trip
        round_trip = request.REQUEST.get('round_trip', False)
        if type (round_trip) is not bool:
            round_trip = (str(round_trip) == 'on')

        route.roundtrip = round_trip
        route.name = request.REQUEST.get('name', 'Untitled')
        route.save()
        route.waypoint_set.all().delete()
        
        waypoints = data.get('waypoints', [])
        if type (waypoints) is not list:
            return HttpResponse('Invalid data c')

        for i in range(len(waypoints)):		
            Waypoint(route = route, index = i, latitude = waypoints[i].get('lat', 0), longitude = waypoints[i].get('lng', 0)).save()
			
        route.calculate_distance()
        return HttpResponseRedirect('/routes/');

