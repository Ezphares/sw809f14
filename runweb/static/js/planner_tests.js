
var planner;

var cassiopeia;
var nytorv;
var randers;

var content;

module('Planner', 
{
	setup: function()
	{
		content = $('#content').html();
	
		planner = new Planner('#map', '#controls', '#info', '');

		cassiopeia = new google.maps.LatLng(57.01312835170527, 9.990901350975037);
		nytorv = new google.maps.LatLng(57.04888899142751, 9.921729862689972);
		randers = new google.maps.LatLng(56.46249048388979, 10.021709203720093);
	},
	teardown: function()
	{
		$('#content').html(content);
	}
});

test('Initialization', function()
{
	expect(2);

	equal(planner.markers.length, 0, 'Route should start without markers');
	equal(planner.route, null, 'No route should start calculated');
});

asyncTest('First marker', function()
{
	expect(2);

	planner.elements.map.on('route-changed', function()
	{
		equal(planner.markers.length, 1, 'route should have one marker');
		equal(planner.route, null, 'no route with one waypoint');
		start();
	});
	
	planner.add_marker(cassiopeia);
});

asyncTest('Second marker', function()
{
	expect(3);

	var count = 0;
	
	planner.elements.map.on('route-changed', function()
	{
		if (++count == 2)
		{
			equal(planner.markers.length, 2, 'route should have two markers');
			equal(planner.route.legs.length, 1, 'route should have 1 leg');
			ok(planner.route.legs[0].distance.value < 10000, 'this route should be less than 10 kilometers (nytorv - randers)');
		}
		start();
	});
	
	planner.add_marker(cassiopeia, true);
	stop();
	planner.add_marker(nytorv);
});

asyncTest('Third marker and clear', function()
{
	expect(6);

	var count = 0;
	
	planner.elements.map.on('route-changed', function()
	{
		if (++count == 3)
		{
			equal(planner.markers.length, 3, 'route should have three markers');
			equal(planner.route.legs.length, 2, 'route should have 2 legs');
			ok(planner.route.legs[0].distance.value < 10000, 'this leg should be less than 10 kilometers (cassiopeia - nytorv)');
			ok(planner.route.legs[1].distance.value > 10000, 'this leg should be more than 10 kilometers (nytorv - randers)');
			planner.clear();
			equal(planner.markers.length, 0, 'markers should be cleared');
			equal(planner.route, null, 'route should be cleared');
		}
		start();
	});
	
	planner.add_marker(cassiopeia, true);
	stop();
	planner.add_marker(nytorv, true);
	stop();
	planner.add_marker(randers);
});

asyncTest('Roundtrips', function()
{
	expect(3);

	var count = 0;
	
	planner.elements.map.on('route-changed', function()
	{
		if (++count == 2)
		{
			equal(planner.markers.length, 2, 'route should have two markers');
			equal(planner.route.legs.length, 2, 'route should have 2 leg');
			ok(planner.route.legs[0].start_location.equals(planner.route.legs[1].end_location), 'route starts and ends at the same point')
		}
		start();
	});
	
	planner.round_trip = true;
	planner.add_marker(cassiopeia, true);
	stop();
	planner.add_marker(nytorv);
});

test('Marker removal', function()
{
	expect(4);
	
	planner.add_marker(cassiopeia, true);
	planner.add_marker(nytorv, true);
	planner.add_marker(randers, true);
	
	equal(planner.markers.length, 3, '3 markers should be added');
	
	// Removing middle marker
	google.maps.event.trigger(planner.markers[1], 'rightclick');
	
	equal(planner.markers.length, 2, 'middle marker should be removed');
	
	ok(planner.markers[0].getPosition().equals(cassiopeia), 'first marker should intact')
	ok(planner.markers[1].getPosition().equals(randers), 'final marker should be intact')
});

asyncTest('Marker overflow', function()
{
	var max = 9;
	var count = 0;
	
	planner.elements.map.on('route-changed', function()
	{
		// Test border values, max - 1, max, max + 1
		if (++count >= max - 1)
		{
			ok(planner.markers.length <= max, 'max markers should not be exceeded (' + count + '/' + max + ')');
		}
			
		start();
	});
	
	for (var i = 0; i < max + 1; i++)
	{
		if (i > 0) stop();
	
		planner.add_marker(cassiopeia, true);
	}
});

test('Bad markers', function()
{
	try
	{
		planner.add_marker();
		ok(false, 'no marker position argument should throw');
	}
	catch (ex)
	{
		ok(true, 'no marker position argument should throw');
	}

	try
	{
		planner.add_marker('a');
		ok(false, 'non-latlng marker positions should throw');
	}
	catch (ex)
	{
		ok(true, 'non-latlng marker positions should throw');
	}
});
