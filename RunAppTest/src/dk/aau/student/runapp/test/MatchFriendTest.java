package dk.aau.student.runapp.test;

import dk.aau.student.runapp.MatchComp;
import dk.aau.student.runapp.MatchFriend;
import dk.aau.student.runapp.PickRoute;
import dk.aau.student.runapp.R;
import dk.aau.student.runapp.RunProgress;
import android.app.Activity;
import android.app.Instrumentation.ActivityMonitor;
import android.app.Instrumentation.ActivityResult;
import android.content.Intent;
import android.os.Bundle;
import android.test.ActivityInstrumentationTestCase2;
import android.widget.Button;

public class MatchFriendTest extends ActivityInstrumentationTestCase2<MatchFriend> 
{
	private Button pickRoute_button;
	private MatchFriend matchFriend;
	
	public MatchFriendTest() {
		super(MatchFriend.class);
	}

	protected void setUp() throws Exception 
	{
		super.setUp();
		
		setActivityInitialTouchMode(false);
		
		matchFriend = getActivity();
		assertFalse(matchFriend.getActivityResultIsReturned());
		assertNull(matchFriend.getActivityResult());
	
	    pickRoute_button = (Button) matchFriend.findViewById(R.id.button_pickRoute);		
				
	}
	
	public void testPickRouteUI() 
	{
		//Mock up of pick route result
		Intent returnIntent = new Intent();
		Bundle returnData = new Bundle();
		returnData.putString("route", "this is a route");
		returnIntent.putExtras(returnData);
		ActivityResult activityResult = new ActivityResult(MatchFriend.RESULT_OK, returnIntent);
		
		// register next activities that need to be monitored.
		ActivityMonitor pickRouteMonitor = getInstrumentation().addMonitor(PickRoute.class.getName(), activityResult, true);
		ActivityMonitor runProgressMonitor = getInstrumentation().addMonitor(RunProgress.class.getName(), null, false);
						
		matchFriend.runOnUiThread(new Runnable() 
		{
		  @Override
		  public void run() 
		  {
		    // click button and open next activity.
		    pickRoute_button.performClick();
		  }
		});
				
		// PickRoute is opened and captured.
		Activity pickRoute = getInstrumentation().waitForMonitorWithTimeout(pickRouteMonitor, 1000);
		//RunProgress is opened and captured
		Activity runProgress = getInstrumentation().waitForMonitorWithTimeout(runProgressMonitor, 5000);
		
		//Check that the results are handled appropriately
		assertTrue(matchFriend.getActivityResultIsReturned());
		assertEquals(matchFriend.getActivityResult(), "this is a route");
		//Check that RunProgress is started
		assertNotNull(runProgress);
		runProgress.finish();
	}
	

}


