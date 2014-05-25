package dk.aau.student.runapp.test;

import android.content.Intent;
import android.os.Bundle;
import android.test.ActivityInstrumentationTestCase2;
import dk.aau.student.runapp.RunProgress;
//import static org.junit.Assert.*;
//import static org.hamcrest.CoreMatchers.*;

public class RunProgressTest extends ActivityInstrumentationTestCase2<RunProgress> 
{
	private RunProgress runProgress;
	
	public RunProgressTest() {
		super(RunProgress.class);
	}

	protected void setUp() throws Exception 
	{
		super.setUp();
		
		setActivityInitialTouchMode(false);
	}
	
	public void test_maps()
	{		
		Intent intent = new Intent();
		Bundle routeData = new Bundle();
		routeData.putString("route", "{\"difficulty\": 0.0, \"id\": 5, \"polyline\": \"sqa{Iyd|{@HyB@a@l@Ht@L?DMzCaB]\", \"name\": \"Short home\", \"waypoints\": [{\"lat\": 57.02953289078507, \"lng\": 9.979815781116486}, {\"lat\": 57.02947742305398, \"lng\": 9.980609714984894}, {\"lat\": 57.029007403694145, \"lng\": 9.980084002017975}], \"round_trip\": true}");
		intent.putExtras(routeData);
		
		setActivityIntent(intent);
		runProgress = getActivity();
		assertNotNull(runProgress.get_map());
		int size = runProgress.get_decoded_route().size();
		assertEquals(size, 8);
		runProgress.finish();
	}
}
