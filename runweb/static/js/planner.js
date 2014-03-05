/**
 * A class representing a route planner, containing a map and tools to add and remove waypoints to a route
 * @class
 * @param {String} map A css selector identifying the element to contain the map
 * @param {String} controls A css selector identifying the element to contain waypoint controls
 * @param {String} info A css selector identifying the element to display route information
 * @param {String} load A css selector identifying an element of the map to load information from. An empty map will be loaded if this element does not exist
 * @param {Number[]} [mapsize] the size of the map in pixels, given as [width, height]
 */
Planner = function(map, controls, info, load, mapsize)
{
	// Mapsize is optional
	mapsize = mapsize || [640, 480];

	/** JQuery selectors of the elements used by the planner */
	this.elements = {'map': $(map), 'controls': $(controls), 'info': $(info), 'load': $(load)};
	/** The google map object */
	this.map = null;
	/** An array of google map markers */
	this.markers = [];
	/** A google maps directions service instance */
	this.directions = new google.maps.DirectionsService();
	/** A google maps directionsrenderer instance */
	this.route_renderer = null;
	/** a google maps route information instance */
	this.route = null;
	/** Whether the route should start and end at the same point */
	this.round_trip = false;
	/** jQuery selector of a container where the route json is placed for upload */
	this.json_container = null;
	
	// Setup map size
	this.elements.map.css({'width': mapsize[0] + 'px',
						   'height': mapsize[1] + 'px'});
						   
	this.elements.info.css({'height': mapsize[1] + 'px'});
						   
	this.initialize_map(this.elements.map[0]);
	this.initialize_controls();
	this.update_info();
};

/**
 * Initializes the google map. First tests whether geolocation is available,
 * and if so, centers the map on the user.
 * <br />Called automatically by constructor.
 * @param {Node} target The html element to contain the map
 */
Planner.prototype.initialize_map = function(target)
{
	// Allow 'this' reference through callbacks
	var planner = this;
	var options = {'center': new google.maps.LatLng(-34.397, 150.644),
				   'zoom': 12};
	
	// Callback function
	var load_map = function()
	{
		console.log(target);
		planner.map = new google.maps.Map(target, options);
		planner.map_events();
		if (planner.elements.load.length)
			planner.load(planner.elements.load.html());
	};

	// Check if geolocation is supported
	if (navigator.geolocation)
	{
		navigator.geolocation.getCurrentPosition(function(pos)
		{
			// Successful geolocation
			options.center = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
			load_map();
		}, function()
		{
			// Failed geolocation. Permission denied?
			load_map();
		});
	}
	else
		// Geolocation was not supported
		load_map();
};

/**
 * Sets up events for map and markers.
 * <br />Called automatically by initialize_map.
 */
Planner.prototype.map_events = function()
{
	// Allow 'this' reference through callbacks
	var planner = this;
	
	// Event to add a waypoint
	google.maps.event.addListener(this.map, 'click', function(ev)
	{
		if (planner.markers.length >= 9)
			return;
		
		// TODO: Create marker function
		var marker_options = {'position': ev.latLng,
							  'draggable': true};
		
		var marker = new google.maps.Marker(marker_options);
		planner.markers.push(marker);
		planner.update_route(planner);
		
		// Event to remove said waypoint
		google.maps.event.addListener(marker, 'rightclick', function(ev)
		{
			marker.setMap();
			
			var index = planner.markers.indexOf(marker);
			if (index >= 0)
				planner.markers.splice(index, 1);
				
			planner.update_route(planner);
		});
		
		// Event on drag
		google.maps.event.addListener(marker, 'dragend', function(ev)
		{
			planner.update_route(planner);
		});
	});
};

/**
 * Updates the route display of the route planner.
 * <br /> Called automatically by several events.
 */
Planner.prototype.update_route = function()
{
	// Set map icons
	for (var i = 0; i < this.markers.length; i++)
	{
		this.markers[i].setIcon(STATIC_URL + 'img/number_' + (i + 1) + '.png');
		this.markers[i].setMap(this.map);
	}

	// Allow 'this' reference through callbacks
	var planner = this;
	
	if (this.markers.length >= 2)
	{
		var plan = []
		// Extract positions. This has the nice side effect of copying the array, so markers are unaffected later on.
		for (var i = 0; i < this.markers.length; i++)
		{
			plan.push(this.markers[i].getPosition());
		}
		
		// If we are round-tripping, end at the last waypoint
		if (this.round_trip)
			plan.push(plan[0]);
		
		// Extract start and end point
		var destination = plan.reverse().shift();
		var origin = plan.reverse().shift();
		
		// Plan now contains intermediate waypoints. Wrap these so google maps understands them
		for (var i = 0; i < plan.length; i++)
		{
			// Using stopover true, because it changes route algorithm to allow turning around on the spot
			plan[i] = {'location': plan[i], 'stopover': true};
		}
		
		var route_options = {'origin': origin,
							 'destination': destination,
							 'waypoints': plan,
							 
							 'travelMode': google.maps.TravelMode.WALKING,
							 'avoidHighways': true,
							 'avoidTolls': true,
							 'optimizeWaypoints': false};
		
		this.directions.route(route_options, function(result, status)
		{
			if (status == google.maps.DirectionsStatus.OK)
			{
				planner.route = result.routes[0];
				
				// Update existing route if possible, otherwise create a new route
				if (planner.route_renderer)
				{
					planner.route_renderer.setDirections(result);
				}
				else
				{
					var direction_options = {'directions': result,
											 'draggable': false,   // We use custom draggable markers instead
											 'map': planner.map,
											 'suppressMarkers': true,
											 'preserveViewport': true}
			
					planner.route_renderer = new google.maps.DirectionsRenderer(direction_options);
				}
				
				planner.update_info();
			}
			else
			{
				// Creating the route somehow failed
				// TODO: Handle nicely
				alert('Directions request failed: ' + status);
			}
		});
	}
	else
	{
		// Remove previous route
		if (this.route_renderer)
		{
			this.route_renderer.setMap();
			this.route_renderer = null;
		}
		this.update_info();
	}
};

/**
 * Initializes the planner controls
 * <br >Called automatically by constructor
 */
Planner.prototype.initialize_controls = function()
{
	// Allow 'this' reference through callbacks
	var planner = this;
	
	$('<button>Clear</button>').appendTo(this.elements.controls).click(function(ev)
	{
		planner.clear();
	});
	
	$('<button>Reverse</button>').appendTo(this.elements.controls).click(function(ev)
	{
		planner.markers.reverse();
		planner.update_route();
	});
	
	$('<label>Round-trip?<input type="checkbox"/></label>').appendTo(this.elements.controls).find('input').change(function(ev)
	{
		planner.round_trip = $(this).is(':checked');
		planner.update_route();
	});
	
	this.json_container = $('<input type="hidden" name="json" />');
	$('<form action="" method="POST"><input type="text" name="name" value="Route name" /><input type="submit" /></form>').append(this.json_container).append(CSRF).appendTo(this.elements.controls);
};

/**
 * Clears route and markers from the map
 */
Planner.prototype.clear = function()
{
	// Clear all markers, avoiding leaks
	for (var i = 0; i < this.markers.length; i++)
	{
		this.markers[i].setMap();
	}
	this.markers = [];
	
	// Clear route
	if (this.route_renderer)
		this.route_renderer.setMap();
		
	this.route_renderer = null;
	
	this.update_info();
};

/**
 * Updates the route information view
 */
Planner.prototype.update_info = function()
{
	this.elements.info.html('');
	
	if (!this.route_renderer)
	{
		$('<span></span>').text("No route entered").appendTo(this.elements.info);
		this.json_container.val('{"waypoints":[]}');
	}
	else
	{
		var distance = 0;
		for (var i = 0; i < this.route.legs.length; i++)
		{
			distance += this.route.legs[i].distance.value;
		}
		$('<span></span>').text("Route distance: " + distance + 'm').appendTo(this.elements.info);
		
		var waypoints = [];
		for (var i = 0; i < this.markers.length; i++)
		{
			waypoints.push({'lat': this.markers[i].getPosition().lat(), 'lng': this.markers[i].getPosition().lng()});
		}
		
		this.json_container.val(JSON.stringify({'waypoints': waypoints,
												'distance': distance})); // TODO: Enter score here
	}
}

/**
 * Loads a route from a json representation
 * @param {JSON} json the json representation to load
 */
Planner.prototype.load = function(json)
{
	var data = JSON.parse(json);
	console.log(data);
	this.elements.controls.find('input[name="name"]').val(data['name']);
	
	var planner = this;
	for (var i = 0; i < data.waypoints.length; i++)
	{
		// TODO: Create marker function
		var marker_options = {'position': new google.maps.LatLng(data.waypoints[i].lat, data.waypoints[i].lng),
							  'draggable': true};
		
		var marker = new google.maps.Marker(marker_options);
		planner.markers.push(marker);
		planner.update_route(planner);
		
		// Event to remove said waypoint
		google.maps.event.addListener(marker, 'rightclick', function(ev)
		{
			marker.setMap();
			
			var index = planner.markers.indexOf(marker);
			if (index >= 0)
				planner.markers.splice(index, 1);
				
			planner.update_route(planner);
		});
		
		// Event on drag
		google.maps.event.addListener(marker, 'dragend', function(ev)
		{
			planner.update_route(planner);
		});
	}
	
	console.log(this.markers);
	this.update_route();
}
