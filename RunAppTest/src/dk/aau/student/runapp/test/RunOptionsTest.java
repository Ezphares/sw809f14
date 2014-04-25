package dk.aau.student.runapp.test;

import dk.aau.student.runapp.MatchComp;
import dk.aau.student.runapp.MatchFriend;
import dk.aau.student.runapp.R;
import dk.aau.student.runapp.RunOptions;
import android.app.Activity;
import android.app.Instrumentation.ActivityMonitor;
import android.test.ActivityInstrumentationTestCase2;
import android.widget.Button;

public class RunOptionsTest extends ActivityInstrumentationTestCase2<RunOptions> 
{
	private RunOptions runOptions;
	private Button runOff_button, runFriend_button;

	public RunOptionsTest() 
	{
		super(RunOptions.class);
	}
	
	 protected void setUp() throws Exception 
	  {
		    super.setUp();
		    
		    setActivityInitialTouchMode(false);
		    
		    //start activity
		    runOptions = getActivity();
		    //get needed button
		    runOff_button = (Button) runOptions.findViewById(R.id.button_runOff);
		    runFriend_button = (Button) runOptions.findViewById(R.id.button_friendlyRun);
	  }
	 
	  public void testMatchComp() 
	  {
	  
		  // register next activity that need to be monitored.
		  ActivityMonitor matchCompMonitor = getInstrumentation().addMonitor(MatchComp.class.getName(), null, false);		  
		  
		  runOptions.runOnUiThread(new Runnable() 
		  {
		    @Override
		    public void run() 
		    {
		      // click button and open next activity.
		      runOff_button.performClick();
		    }
		  });

		  // next activity is opened and captured.
		  Activity matchComp = getInstrumentation().waitForMonitorWithTimeout(matchCompMonitor, 5000);
		  //Check that we actually start an activity!
		  assertNotNull(matchComp);
		  matchComp.finish();
		  
	  }
	  
	  public void testMatchFriend()
	  {
		  // register next activity that need to be monitored.
		  ActivityMonitor matchFriendMonitor = getInstrumentation().addMonitor(MatchFriend.class.getName(), null, false);

		  runOptions.runOnUiThread(new Runnable() 
		  {
		    @Override
		    public void run() 
		    {
		      // click button and open next activity.
		      runFriend_button.performClick();
		    }
		  });

		  // next activity is opened and captured.
		  Activity matchFriend = getInstrumentation().waitForMonitorWithTimeout(matchFriendMonitor, 5000);
		  //we good here?
		  assertNotNull(matchFriend);
		  matchFriend.finish();
		  
	  }

}
