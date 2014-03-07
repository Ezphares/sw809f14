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
	
	if (this.elements.map.length > 0)
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
		planner.add_marker(ev.latLng)
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
		if (typeof STATIC_URL != 'undefined')
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
			
			// Trigger event, mainly for unit testing, but could be useful later.
			planner.elements.map.trigger('route-changed');
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
		
		this.route = null;
		this.update_info();
		
		// Trigger event, mainly for unit testing, but could be useful later.
		this.elements.map.trigger('route-changed');
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
	
	// TODO: Add checkbox to form or json container
	var checkbox = $('<label>Round-trip?<input name="round_trip" type="checkbox"/></label>');
	checkbox.find('input').change(function(ev)
	{
		planner.round_trip = $(this).is(':checked');
		planner.update_route();
	});
	
	this.json_container = $('<input type="hidden" name="json" />');
	
	var form = $('<form action="" method="POST"><input type="text" name="name" value="Route name" /><input type="submit" /></form>').prepend(checkbox).append(this.json_container).appendTo(this.elements.controls);
	if (typeof CSRF != 'undefined')
		form.append(CSRF);
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
	this.route = null;
	
	this.update_info();
};

/**
 * Updates the route information view
 */
Planner.prototype.update_info = function()
{
	if (this.elements.info.length == 0)
		return;

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
	// Most invalid json should either throw during parsing or in the waypoint for loop.
	// Minor problems such as missing names produce reasonable results as it is
	var data = JSON.parse(json);
	this.elements.controls.find('input[name="name"]').val(data.name);
	this.round_trip = !!data.round_trip;
	this.elements.info.find('input[name="rund_trip"]').prop('checked', this.round_trip);
	
	for (var i = 0; i < data.waypoints.length; i++)
	{
		if (typeof data.waypoints[i].lat != 'number' || typeof data.waypoints[i].lng != 'number')
			throw 'Attempting to load bad waypoint data';
			
		this.add_marker(new google.maps.LatLng(data.waypoints[i].lat, data.waypoints[i].lng), true)
	}
	
	this.update_route();
}

/**
 * Adds a marker to the map, adding relevant events and updates the directions
 * @param {google.maps.LatLng} position The LatLng object representing the position to add the marker
 * @param {Bool} [supress_directions] If true, the directions service will not be invoked. This is used when bulk adding markers,
 *		such as when loading a route form database, or during unit testing. update_route() should be called manually after all markers are added.
 */
Planner.prototype.add_marker = function(position, supress_directions)
{
	// We only need to test if the latlng exists, google will test validity
	if (!position)
		throw "No marker position given"

	// Allow 'this' reference through callbacks
	var planner = this;

	if (this.markers.length >= 9)
	{
		this.elements.map.trigger('route-changed');
		return;
	}
	
	var marker_options = {'position': position,
						  'draggable': true};
	
	var marker = new google.maps.Marker(marker_options);
	this.markers.push(marker);
	
	if (supress_directions)
	{
		this.elements.map.trigger('route-changed');
	}
	else
	{
		this.update_route();
	}
	
	// Event to remove the marker waypoint
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
};
